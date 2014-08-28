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

HTTPERROR_ALLOW_ALL = True