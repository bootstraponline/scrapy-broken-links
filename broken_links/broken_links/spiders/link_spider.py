# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.utils.sitemap import Sitemap
from broken_links.items import BrokenLinksItem

import urllib2

# Follows urls on target domain and saves url, status, and referrer.
#
# note that target_domain must not have http://
#
# scrapy crawl link_spider -o items.json
#                          -a arg_start_urls=url/to/start_urls.txt
#                          -a arg_target_domain=example.com
class LinkSpiderSpider(CrawlSpider):
    name = "link_spider"

    # __init__ is called to get the spider name so avoid doing any extra work
    # in init such as downloading files.
    #
    # args are automatically made available to the spider.

    def start_requests(self):
        self.rules = (
            Rule(LinkExtractor(allow_domains=['aquent.com'], unique=True),
                 callback=self.parse_item,
                 process_links=self.clean_links,
                 follow=True),
        )
        self._compile_rules()

        yield scrapy.Request('http://www.aquent.com', dont_filter=True)

    # rule process_links callback
    def clean_links(self, links):
        for link in links:
            # remove html fragment (#) and query params (?)
            link.fragment = ''
            link.url = link.url.split('#')[0].split('?')[0]
            yield link

    # rule callback
    def parse_item(self, response):
        item = BrokenLinksItem()
        item['url'] = response.url
        item['status'] = response.status
        yield item