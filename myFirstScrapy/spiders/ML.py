# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from myFirstScrapy.items_ml import *
from scrapy.spiders import CrawlSpider


def numeroPagina(cant):
    inicio=1
    for i in range(1, int(cant)):
        url = "https://computacion.mercadolibre.com.ar/pc-escritorio/pc/_Desde_"+str(50+inicio)
        inicio+=50
        yield url


class MlSpider(CrawlSpider):
    name = 'ML'
    allowed_domains = ['www.mercadolibre.com.ar']
    start_urls = ['http://www.mercadolibre.com.ar/',
                  'https://computacion.mercadolibre.com.ar/pc-escritorio/pc/'] + list(numeroPagina(10))

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=(' // *[ @ id = "searchResults"]',)),
             callback="parse",
             follow=True),)

    def parse(self, response):
        itemName = response.xpath('//div// a / div / h2 / span[1]/text()').extract()
        itemPrice = response.xpath('//div// a / div / div[1] / span[2]/text()').extract()
        itemURL = response.xpath('//div/a/@href').extract()
        item = Item_ML()

        for i in range(0, len(itemName)):
            item['articulo'] = itemName[i]
            item['precio'] = itemPrice[i]
            item['url'] = itemURL[i]
            item['urlph'] = str(response.url)
            yield item
