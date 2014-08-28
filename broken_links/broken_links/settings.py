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

# Allow saving non-200 status codes.
HTTPERROR_ALLOW_ALL = True

# Make sure the crawler doesn't cause problems for the servers.
# http://doc.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 10.0 # default is 5
AUTOTHROTTLE_MAX_DELAY = 120.0 # default is 60