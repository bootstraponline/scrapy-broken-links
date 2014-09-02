#### notes

[scrapy hipchat](http://www.hipchat.com/gCvqSX8IC)

```bash
scrapy shell http://www.google.com
```

```python
import inspect
inspect.getmembers(response)
```

run from the project directory (broken_links/broken_links$ )
note that this will append to the items.json file if it exists instead of overriding.

```
rm items.json
scrapy crawl link_spider -o items.json -a arg_start_urls=https://raw.githubusercontent.com/bootstraponline/scrapy-broken-links/gh-pages/scrapy/start_urls.txt -a arg_target_domain=https://raw.githubusercontent.com/bootstraponline/scrapy-broken-links/gh-pages/scrapy/target_domain.txt
cat items.json
```

```
arg_start_urls

https://raw.githubusercontent.com/bootstraponline/scrapy-broken-links/gh-pages/scrapy/start_urls.txt -a 

arg_target_domain

https://raw.githubusercontent.com/bootstraponline/scrapy-broken-links/gh-pages/scrapy/target_domain.txt

```

- http://doc.scrapy.org/en/latest/topics/settings.html#std:setting-DOWNLOAD_DELAY
- http://doc.scrapy.org/en/latest/topics/link-extractors.html#topics-link-extractors


> "rules
Which is a list of one (or more) Rule objects. Each Rule defines a certain behaviour for crawling the site. Rules objects are described below. If multiple rules match the same link, the first one will be used, according to the order they’re defined in this attribute."
>
> - http://doc.scrapy.org/en/latest/topics/spiders.html#scrapy.contrib.spiders.Rule
 

Make sure the crawler doesn't cause problems.

- http://doc.scrapy.org/en/latest/topics/autothrottle.html
- https://github.com/scrapy/scrapy/blob/e62bbf0766568b902f99d963030e57b96cc2aae6/tests/test_spider.py

```python
Link(url='http://www.github.com/', text='valid github link', fragment='', nofollow=False)
log.msg(repr(links[0]), level=log.INFO)
log.msg('------------------------------- Parsing: %s' % response.url, level=log.INFO)
```


Args can be set on scraping hub

![](args_on_scrapinghub.png)
