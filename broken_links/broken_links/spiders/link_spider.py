# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from broken_links.items import BrokenLinksItem

import urllib2

class LinkSpiderSpider(CrawlSpider):
    name = "link_spider"

    # urllib2 is sync however we're only using these methods once to initialize the crawler.
    @staticmethod
    def remote_file_to_string(url):
        # read, split, filter, return first non-empty line.
        return filter(None, urllib2.urlopen(url).read().splitlines())[0]

    @staticmethod
    def remote_file_to_array(url):
        # read, split, filter, return all non-empty lines
        return filter(None, urllib2.urlopen(url).read().splitlines())

    def __init__(self, target_domain=None, start_urls=None, *args, **kwargs):
        # set start urls property on the spider
        self.start_urls = self.remote_file_to_array(start_urls)
        print 'Start urls: ', self.start_urls

        # load target domain and then use it once to define the rules
        target_domain = self.remote_file_to_string(target_domain)
        print 'Target domain:', target_domain

        # If a link matches multiple rules, the first rule wins.
        self.rules = (
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

        # must init **after** setting self.start_urls / self.rules
        # otherwise the crawler will do nothing.
        super(LinkSpiderSpider, self).__init__(*args, **kwargs)

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
        item['referer'] = response.request.headers['Referer']
        yield item