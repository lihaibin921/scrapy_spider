# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import scrapy_spider.utils.pathutil as pathutil


class ScrapySpiderPipeline:
    def process_item(self, item, spider):
        return item


"""
    4399最新小游戏 写入csv 
"""


class GameNewWritePipeline():
    csv_url = pathutil.get_abs_path(r'datas/game_new/data.csv')

    def __init__(self):
        # 暂存数据集
        self.data_list = []
        self.write_count = 0
        self.data_count = 0

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if item is None:
            return item

        self.data_list.append(item)
        self.data_count += 1

        # 每100行数据追加进csv文件 清空数据集
        if len(self.data_list) >= 100:
            df = pd.DataFrame(self.data_list)
            df.to_csv(GameNewWritePipeline.csv_url, index=False, header=False, sep=',', mode='a', encoding='utf-8')
            self.data_list = []
            self.write_count += 1

        return item

    def close_spider(self, spider):
        # 将所有剩余数据写入csv
        df = pd.DataFrame(self.data_list)
        df.to_csv(GameNewWritePipeline.csv_url, index=False, header=False, sep=',', mode='a', encoding='utf-8')
        print(f'共写入csv {self.write_count} 次 , 写入 {self.data_count} 条数据')
