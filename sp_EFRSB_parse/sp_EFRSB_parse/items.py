# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SpEfrsbParseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class InfoActItem(scrapy.Item):
    trade_id = scrapy.Field()
    url = scrapy.Field()
    start_price = scrapy.Field()
    description = scrapy.Field()
    classifier = scrapy.Field()
    final_price = scrapy.Field()
    date = scrapy.Field()
    winner = scrapy.Field()
    justification = scrapy.Field()
    