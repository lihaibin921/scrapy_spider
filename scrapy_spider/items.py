# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapySpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class GameNewItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    type = scrapy.Field()
    time = scrapy.Field()
    img = scrapy.Field(serializer=str)
