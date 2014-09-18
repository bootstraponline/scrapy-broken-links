# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from broken_links.items import BrokenLinksItem

import re

# scrapy crawl link_spider -o items.json
class LinkSpiderSpider(CrawlSpider):
    name = "link_spider"

    def start_requests(self):
        # self.arg_email = 'example@example.com' # set via argument on scrapinghub.com
        self.arg_password = '..password..'

        # url *must* start with the string
        allow_urls = ['https://accounts.google.com/ServiceLogin?', 'https://sites.google.com/']
        allow_regex_array = ["^" + re.escape(url) for url in allow_urls]

        # allow partial matches, don't force the url to start with the string
        deny_urls = ['/system/app/pages/recentChanges',
                     '/system/app/pages/meta/',
                     '/system/app/pages/removeAccess',
                     '/system/app/pages/reportAbuse']
        deny_regex_array = [re.escape(url) for url in deny_urls]

        #
        # must allow sitemap
        # /system/app/pages/sitemap/hierarchy
        #
        # most other system app pages we want to deny.

        self.rules = [
            Rule(LinkExtractor(allow=allow_regex_array, deny=deny_regex_array),
                 callback=self.parse_item,
                 follow=True),
            # Don't follow any external domain links.
            Rule(LinkExtractor(unique=True),
                 callback=self.parse_item,
                 follow=False),
        ]
        self._compile_rules()

        url = 'https://sites.google.com/a/subdomain.example.com/target/'
        # This request is not processed through the rules. The callback must be set manually
        # or it'll never reach self.parse_item
        yield scrapy.Request(url, dont_filter=True, callback=self.parse_item)

    def authenticate_google(self, response):
        # works on both /ServiceLogin and /AccountChooser
        return scrapy.FormRequest.from_response(
            response,
            formdata={'Email': self.arg_email, 'Passwd': self.arg_password},
            dont_filter=True
        )

    # rule/request callback
    def parse_item(self, response):
        url = response.url
        requires_auth = url.startswith('https://accounts.google.com/ServiceLogin?') or \
                        url.startswith('https://accounts.google.com/AccountChooser')
        if requires_auth:
            yield self.authenticate_google(response)
        else:
            item = BrokenLinksItem()
            item['url'] = url
            item['status'] = response.status
            item['referer'] = response.request.headers['Referer']
            item['link_text'] = response.meta.get('link_text')
            yield item
