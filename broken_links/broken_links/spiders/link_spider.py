# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.utils.sitemap import Sitemap
from broken_links.items import BrokenLinksItem

import urllib2

# Follows urls on target domain and saves url, status, and referer.
#
# scrapy crawl link_spider -o items.json
#                          -a arg_start_urls=url/to/start_urls.txt
#                          -a arg_target_domain=url/to/target_domain.txt
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

    @staticmethod
    def sitemap_to_array(url):
        results = []
        body = urllib2.urlopen(url).read()
        sitemap = Sitemap(body)
        for item in sitemap:
            results.append(item['loc'])
        return results


    # __init__ is called to get the spider name so avoid doing any extra work
    # in init such as downloading files.
    #
    # args are automatically made available to the spider.

    def start_requests(self):
        # update rules
        # load target domain and then use it once to define the rules
        target_domain = self.remote_file_to_string(self.arg_target_domain)
        print 'Target domain: ', target_domain

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
        self._compile_rules()

        # now deal with requests
        start_urls = []
        if self.arg_start_urls.endswith('.xml'):
            print 'sitemap detected!'
            start_urls = self.sitemap_to_array(self.arg_start_urls)
        else:
            start_urls = self.remote_file_to_array(self.arg_start_urls)
        print 'Start urls: ', start_urls
        # must set dont_filter on the start_urls requests otherwise
        # they will not be recorded in the items output because it'll
        # be considered a duplicate url.
        # see https://github.com/scrapy/scrapy/blob/5daa14770b23da250ccfd4329899a1c3f669b1f3/scrapy/spider.py#L65
        for url in start_urls:
            yield scrapy.Request(url, dont_filter=True)

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