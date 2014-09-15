# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.utils.sitemap import Sitemap
from broken_links.items import BrokenLinksItem

import urllib2
import re

# scrapy crawl link_spider -o items.json
class LinkSpiderSpider(CrawlSpider):
    name = "link_spider"

    def start_requests(self):
        print "---- start_requests"
        self.arg_email = 'example@example.com'
        self.arg_password = '..password..'

        allow_url_fragments = ['https://accounts.google.com/ServiceLogin?', 'https://sites.google.com/']
        allow_rgx_array = []

        for fragment in allow_url_fragments:
            allow_rgx_array.append("^" + re.escape(fragment) + ".*")

        self.rules = (
            Rule(LinkExtractor(allow=allow_rgx_array, unique=True),
                 callback=self.parse_item,
                 follow=True),
        )
        self._compile_rules()

        url = 'https://sites.google.com/a/subdomain.example.com/target/'
        print "starting: ", url
        # start_requests isn't processed through the rules... so we must manually invoke the callback.
        yield scrapy.Request(url, dont_filter=True, callback=self.parse_item)

    def authenticate_google(self, response):
        print "--------------------- Authenticating for: ", response.url
        # works on both /ServiceLogin and /AccountChooser
        return scrapy.FormRequest.from_response(
            response,
            formdata={'Email': self.arg_email, 'Passwd': self.arg_password},
            callback=self.parse_item,
            dont_filter=True
        )

    # rule callback
    def parse_item(self, response):
        print "--------------------- parsing: ", response.url
        # url requires authentication
        url = response.url
        requires_auth = url.startswith('https://accounts.google.com/ServiceLogin?') or url.startswith('https://accounts.google.com/AccountChooser')
        if requires_auth:
            print "---- invoking auth google"
            yield self.authenticate_google(response)
        else:
            print "---- saving link item"
            item = BrokenLinksItem()
            item['url'] = url
            item['status'] = response.status
            item['referer'] = response.request.headers['Referer']
            yield item
