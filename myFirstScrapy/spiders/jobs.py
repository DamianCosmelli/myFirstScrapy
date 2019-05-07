# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.selector import Selector
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule
from myFirstScrapy.items import *

class JobsSpider(CrawlSpider):
    exclude = ['type', 'location', 'category']
    name = 'jobs'
    allowed_domains = ['www.python.org']
    start_urls = ['http://www.python.org/',
                  'https://www.python.org/jobs/']

    rules = (
        Rule(LinkExtractor(allow=(), restrict_css=('.list-recent-jobs',)),
             callback="parse_item",
             follow=True),)

    def parse_item(self, response):
        if not (str(response.url).__contains__('location')
                or str(response.url).__contains__('type')
                or str(response.url).__contains__('category')):
            itemlink = str(response.css('.text > .listing-company > .listing-company-name > .company-name::text').extract()[0]).replace('\\n\\t', ' ').replace('\\t', ' ').replace('\\n', ' ').replace(',', ' ').strip()

            item = MyfirstscrapyItem()
            item['puesto'] = itemlink
            item['url'] = str(response.url)
            yield item
