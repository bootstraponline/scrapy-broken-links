# -*- coding: utf-8 -*-
import scrapy


class LinkSpiderSpider(scrapy.Spider):
    name = "link_spider"
    allowed_domains = ["http://bootstraponline.github.io/scrapy-broken-links/"]
    start_urls = (
        'http://www.http://bootstraponline.github.io/scrapy-broken-links//',
    )

    def parse(self, response):
        pass
