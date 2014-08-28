scrapy shell http://www.google.com
import inspect
inspect.getmembers(response)

run from the project directory (broken_links/broken_links$ )
note that this will append to the items.json file if it exists instead of overriding.

rm items.json; scrapy crawl link_spider -o items.json; cat items.json

todo: configure download delay
http://doc.scrapy.org/en/latest/topics/settings.html#std:setting-DOWNLOAD_DELAY

todo: process links to remove html fragments and query parameters
http://doc.scrapy.org/en/latest/topics/link-extractors.html#topics-link-extractors
http://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.contrib.spiders.Rule

https://github.com/scrapy/scrapy/blob/e62bbf0766568b902f99d963030e57b96cc2aae6/tests/test_spider.py

Link(url='http://www.github.com/', text='valid github link', fragment='', nofollow=False)
log.msg(repr(links[0]), level=log.INFO)
log.msg('------------------------------- Parsing: %s' % response.url, level=log.INFO)