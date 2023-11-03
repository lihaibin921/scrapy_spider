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


class BiliUserItem(scrapy.Item):
    uid = scrapy.Field(serializer=int)
    name = scrapy.Field()
    sex = scrapy.Field()
    face = scrapy.Field()
    sign = scrapy.Field()
    rank = scrapy.Field()
    level = scrapy.Field()
    jointime = scrapy.Field()
    coins = scrapy.Field()
    birthday = scrapy.Field()

    vip_type = scrapy.Field()
    vip_status = scrapy.Field()
    vip_due_date = scrapy.Field()
    vip_label = scrapy.Field()

    official_role = scrapy.Field()
    official_title = scrapy.Field()
    official_desc = scrapy.Field()
    official_type = scrapy.Field()

    # 记录是否爬取失败 用于pipeline处理
    crawl_status = scrapy.Field(serializer=bool)
