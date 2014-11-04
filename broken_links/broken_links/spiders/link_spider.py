# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from broken_links.items import BrokenLinksItem

class LinkSpiderSpider(CrawlSpider):
    name = "link_spider"

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