# -*- coding: utf-8 -*-
import scrapy
from broken_links.items import BrokenLinksItem
from urlparse import urlparse

# scrapy runspider link_spider.py
#
# run from the project directory (broken_links/broken_links$ )
# scrapy crawl link_spider -o items.json
class LinkSpiderSpider(scrapy.Spider):
    # todo: configure download delay
    # http://doc.scrapy.org/en/latest/topics/settings.html#std:setting-DOWNLOAD_DELAY
    name = "link_spider"
    allowed_domains = ["bootstraponline.github.io", "www.github.com"]
    start_urls = (
        'http://bootstraponline.github.io/scrapy-broken-links/',
    )

    def parse(self, response):
        item = BrokenLinksItem()
        item['url'] = response.url
        item['status'] = response.status
        item['parent'] = response.request.url
        # from http://doc.scrapy.org/en/latest/topics/spiders.html#topics-spiders
        for url in response.xpath('//a/@href').extract():
            # ensure url has a valid scheme before attempting to crawl it.
            if urlparse(url).scheme != '':
                yield scrapy.Request(url, callback=self.parse)