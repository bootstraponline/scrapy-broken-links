# -*- coding: utf-8 -*-
import scrapy

# scrapy runspider link_spider.py
# scrapy crawl link_spider -o items.json
class LinkSpiderSpider(scrapy.Spider):
    # todo: configure download delay
    # http://doc.scrapy.org/en/latest/topics/settings.html#std:setting-DOWNLOAD_DELAY
    name = "link_spider"
    allowed_domains = ["http://bootstraponline.github.io/scrapy-broken-links/", "http://www.github.com"]
    start_urls = (
        'http://bootstraponline.github.io/scrapy-broken-links/',
    )

    # limit crawling to allowed domains only
    # http://doc.scrapy.org/en/latest/topics/spider-middleware.html#scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware
    SPIDER_MIDDLEWARES = {
        'scrapy.contrib.spidermiddleware.offsite.OffsiteMiddleware': 1,
    }

    def parse(self, response):
        item = scrapy.Item()
        item['url'] = response.url
        item['status'] = response.status
        item['parent'] = response.request.url
        # from http://doc.scrapy.org/en/latest/topics/spiders.html#topics-spiders
        for url in response.xpath('//a/@href').extract():
            yield scrapy.Request(url, callback=self.parse)