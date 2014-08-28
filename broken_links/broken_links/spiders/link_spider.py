# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from broken_links.items import BrokenLinksItem

class LinkSpiderSpider(CrawlSpider):
    name = "link_spider"
    target_domain = "bootstraponline.github.io"

    start_urls = (
        'http://bootstraponline.github.io/scrapy-broken-links/',
    )

    # If a link matches multiple rules, the first rule wins.
    rules = (
        # If a link is within the target domain, follow it.
        Rule(LinkExtractor(allow_domains=[target_domain], unique=True),
             callback='parse_item',
             process_links='clean_links',
             follow=True),
        # Don't follow any external domain links.
        Rule(LinkExtractor(unique=True),
             callback='parse_item',
             process_links='clean_links',
             follow=False),
    )

    def clean_links(self, links):
        for link in links:
            # remove html fragment (#) and query params (?)
            link.fragment = ''
            link.url = link.url.split('#')[0].split('?')[0]
            yield link

    def parse_item(self, response):
        item = BrokenLinksItem()
        item['url'] = response.url
        item['status'] = response.status
        item['referer'] = response.request.headers['Referer']
        yield item