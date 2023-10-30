# encoding: utf-8
# @Time : 2023/10/29 23:34
# @Auther : ISLEY
# @File : game_new_spider.py
# @DESC : 4399 最新游戏爬虫

import scrapy

from scrapy_spider.items import GameNewItem


class GameSpider(scrapy.Spider):
    name = "game_new"
    allowed_domains = ['4399.com']
    custom_settings = {
        "DOWNLOAD_DELAY": "5",
        "ITEM_PIPELINES": {
            "scrapy_spider.pipelines.GameNewWritePipeline": 300
        }
    }

    def start_requests(self):
        urls = ['https://www.4399.com/flash/new.htm']
        for idx in range(2, 11):
            urls.append(f'https://www.4399.com/flash/new_{idx}.htm')
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        games = response.xpath("//ul[@class='n-game cf'][1]/li")  # type: list[scrapy.Selector]

        for game in games:
            item = GameNewItem()
            item['name'] = game.xpath('a/b/text()').get()
            item['url'] = game.xpath('a/@href').get()
            item['type'] = game.xpath('em[1]/a/text()').get()
            item['time'] = game.xpath('em[2]/text()').get()
            item['img'] = game.xpath('a/img/@lz_src').get()
            # print(item)
            yield item
