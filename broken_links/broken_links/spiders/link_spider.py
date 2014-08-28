# -*- coding: utf-8 -*-
import scrapy
from scrapy import log
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from broken_links.items import BrokenLinksItem

# scrapy shell http://www.google.com
# import inspect
# inspect.getmembers(response)
#
# run from the project directory (broken_links/broken_links$ )
# note that this will append to the items.json file if it exists instead of overriding.
#
# rm items.json; scrapy crawl link_spider -o items.json; cat items.json
class LinkSpiderSpider(CrawlSpider):
    # todo: configure download delay
    # http://doc.scrapy.org/en/latest/topics/settings.html#std:setting-DOWNLOAD_DELAY
    name = "link_spider"
    target_domain = "bootstraponline.github.io"

    start_urls = (
        'http://bootstraponline.github.io/scrapy-broken-links/',
    )

    # todo: process links to remove html fragments and query parameters
    # http://doc.scrapy.org/en/latest/topics/link-extractors.html#topics-link-extractors
    # http://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.contrib.spiders.Rule
    rules = (
        Rule(LinkExtractor(allow_domains=[target_domain], unique=True), callback='parse_item',
             process_links='clean_links', follow=True),
        Rule(LinkExtractor(deny_domains=[target_domain], unique=True), callback='parse_item',
             process_links='clean_links', follow=False),
    )

    # https://github.com/scrapy/scrapy/blob/e62bbf0766568b902f99d963030e57b96cc2aae6/tests/test_spider.py
    def clean_links(self, links):
        # Link(url='http://www.github.com/', text='valid github link', fragment='', nofollow=False)
        # log.msg(repr(links[0]), level=log.INFO)
        for link in links:
            # remove html fragment (#) and query params (?)
            link.fragment = ''
            link.url = link.url.split('#')[0].split('?')[0]
            yield link

    def parse_item(self, response):
        # log.msg('------------------------------- Parsing: %s' % response.url, level=log.INFO)
        item = BrokenLinksItem()
        item['url'] = response.url
        item['status'] = response.status
        item['referer'] = response.request.headers['Referer']

        yield item