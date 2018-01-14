# -*- coding: utf-8 -*-

# Scrapy settings for broken_links project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'broken_links'

SPIDER_MODULES = ['broken_links.spiders']
NEWSPIDER_MODULE = 'broken_links.spiders'

# Custom useragent to enable easy server side monitoring
USER_AGENT = "scrapy_link_spider"

# Allow saving non-200 status codes.
HTTPERROR_ALLOW_ALL = True

# Make sure the crawler doesn't cause problems for the servers.
# http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5 # default is 5
AUTOTHROTTLE_MAX_DELAY = 10 * 60 # default is 60

# http://doc.scrapy.org/en/latest/topics/downloader-middleware.html#std:setting-COOKIES_DEBUG
COOKIES_DEBUG = False

# chrome on mac
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36'