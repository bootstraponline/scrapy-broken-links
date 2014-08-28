# -*- coding: utf-8 -*-
import scrapy
from scrapy import log
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from broken_links.items import BrokenLinksItem

# scrapy runspider link_spider.py
#
# run from the project directory (broken_links/broken_links$ )
# note that this will append to the items.json file if it exists instead of overriding.
#
# scrapy crawl link_spider -o items.json
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
        Rule(LinkExtractor(allow_domains=[target_domain], unique=True), callback='parse_item', follow=True),
        Rule(LinkExtractor(deny_domains=[target_domain], unique=True), callback='parse_item', follow=False),
    )

    def parse_item(self, response):
        log.msg('------------------------------- Parsing: %s' % response.url, level=log.INFO)
        item = BrokenLinksItem()
        item['url'] = response.url
        item['status'] = response.status
        item['parent'] = response.request.url

        yield item