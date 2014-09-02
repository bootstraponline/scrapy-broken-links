# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from broken_links.items import BrokenLinksItem

import urllib2

class LinkSpiderSpider(CrawlSpider):
    name = "link_spider"

    # urllib2 is sync however we're only using these methods once to initialize the crawler.
    def remote_file_to_string(url):
        # read, split, filter, return first non-empty line.
        return filter(None, urllib2.urlopen(url).read().splitlines())[0]

    def remote_file_to_array(url):
        # read, split, filter, return all non-empty lines
        return filter(None, urllib2.urlopen(url).read().splitlines())

    # todo: load url from argument to the crawler
    target_domain = remote_file_to_string('https://raw.githubusercontent.com/bootstraponline/scrapy-broken-links/gh-pages/scrapy/start_urls.txt')

    start_urls = remote_file_to_array('https://raw.githubusercontent.com/bootstraponline/scrapy-broken-links/gh-pages/scrapy/start_urls.txt')

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