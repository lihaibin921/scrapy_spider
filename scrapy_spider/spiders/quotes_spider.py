# encoding: utf-8
# @Time : 2023/10/28 17:25
# @Auther : ISLEY
# @File : quotes_spider.py
# @DESC : scrapy官方第一个例子

import scrapy
from pathlib import Path

"""
    quotes 
        爬取urls 直接存html
    quotes2 
        爬取少量信息 直接存json
        
    算是官方给的了解scrapy的例子 , 基本了解下功能
    执行方法在 控制台
        scrapy crawl quotes
        也可以直接在控制台爬链接
        scrapy shell 'https://quotes.toscrape.com/page/1/>'     
"""


class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        urls = [
            "https://quotes.toscrape.com/page/1/",
            "https://quotes.toscrape.com/page/2/"
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = f"quotes-{page}.html"
        Path(filename).write_bytes(response.body)
        self.log(f"Saved file {filename}")


class QuotesSpider2(scrapy.Spider):
    name = "quotes2"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/"
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                "text": quote.css("span.text::text").get(),
                "author": quote.css("small.author::text").get(),
                "tags": quote.css("div.tags a.tag::text").getall()
            }
