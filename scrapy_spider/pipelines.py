# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pandas as pd
import scrapy_spider.utils.pathutil as pathutil
import pymysql
from scrapy_spider.settings import DATABASE_BILI_SETTINGS
from scrapy_spider.items import BiliUserItem, BiliLiveUserItem
from scrapy_spider.spiders.bili_user_spider import BiliUserSpider
from scrapy_spider.spiders.bili_live_user_spider import BiliLiveUserSpider
import logging


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


"""
    bili_user表写入数据
        BiliLiveUserSpider 和 BiliUserSpider公用, 兼容一下好了, 不重新写一个Pipeline 
        可读性差点
"""


class BiliUsersSavePipeline():
    def __init__(self):
        self.conn = pymysql.connect(
            host=DATABASE_BILI_SETTINGS['db_host'],
            port=DATABASE_BILI_SETTINGS['db_port'],
            user=DATABASE_BILI_SETTINGS['db_user'],
            password=DATABASE_BILI_SETTINGS['db_password'],
            database=DATABASE_BILI_SETTINGS['db_name'],
            charset='utf8'  # 注意必须是utf8 不是utf-8
        )
        self.cur = self.conn.cursor()
        self.data_to_insert = []  # 用列表缓存下, 执行批量插入
        self.count = 0
        self.fail_count = 0

    def open_spider(self, spider):
        pass

    def process_item(self, item, spider):
        if isinstance(item, BiliUserItem):
            crawl_status = item['crawl_status']
            if crawl_status:
                # 数据有效 , 批量插入用户表
                self.data_to_insert.append((
                    item['uid'], item['name'], item['sex'], item['face'], item['sign'], item['rank'], item['level'],
                    item['jointime'], item['coins'], item['birthday'], item['vip_type'], item['vip_status'],
                    item['vip_due_date'], item['vip_label'],
                    item['official_role'], item['official_title'], item['official_desc'], item['official_type']
                ))
                self.count += 1
                if len(self.data_to_insert) >= 100:
                    self._insert_datas(self.data_to_insert)
                    self.data_to_insert = []
                logging.info(f"爬取成功:  {item['uid']} , {item['name']}")

            else:
                # 数据无效, 存uid进失败表
                self.fail_count += 1
                self._insert_fail_data(item['uid'])
        elif isinstance(item, BiliLiveUserItem):
            crawl_status = item['crawl_status']
            if crawl_status:
                # 数据有效 , 批量插入用户表
                self.data_to_insert.append((
                    item['uid'], item['name'], item['sex'], item['face'], item['official_desc'], item['official_type'],
                    item['follower']
                ))
                self.count += 1
                if len(self.data_to_insert) >= 100:
                    self._insert_live_datas(self.data_to_insert)
                    self.data_to_insert = []
                logging.info(f"爬取成功:  {item['uid']} , {item['name']}")

            else:
                # 数据无效, 存uid进失败表
                self.fail_count += 1
                self._insert_fail_data(item['uid'])

    def close_spider(self, spider):
        # 清空数据列表 存入DB
        if self.data_to_insert:
            if isinstance(spider, BiliUserSpider):
                self._insert_datas(self.data_to_insert)
            elif isinstance(spider, BiliLiveUserSpider):
                self._insert_live_datas(self.data_to_insert)
        self.conn.close()

    def _insert_datas(self, datas):
        try:
            # 注意rank是关键字 需要``括起来
            insert_sql = ("INSERT IGNORE INTO bili_user(uid , name , sex, face , sign , `rank` , level , jointime ,"
                          " coins , birthday , vipType , vipStatus , VipDueDate , VipLabel , officialRole, officialTitle , officialDesc , officialType) "
                          "VALUES (%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s ,%s, %s ,%s ,%s ,%s)")
            self.cur.executemany(insert_sql, datas)
            self.conn.commit()
            logging.info(f'入库成功 总条数:{self.count} , 失败数:{self.fail_count}')
        except pymysql.Error as e:
            logging.error(f'bili_user数据写入数据库异常 {e}')

    def _insert_live_datas(self, datas):
        # 存入直播接口获得的up主信息, 信息量更少
        try:
            # 注意rank是关键字 需要``括起来
            insert_sql = (
                "INSERT IGNORE INTO bili_user(uid , name , sex, face , officialDesc , officialType , follower) "
                "VALUES (%s ,%s ,%s ,%s ,%s ,%s ,%s)")
            self.cur.executemany(insert_sql, datas)
            self.conn.commit()
            logging.info(f'入库成功 总条数:{self.count} , 失败数:{self.fail_count}')
        except pymysql.Error as e:
            logging.error(f'bili_user数据写入数据库异常 {e}')

    def _insert_fail_data(self, uid):
        try:
            insert_sql = "INSERT IGNORE INTO bili_user_fail (uid) VALUES (%s)"
            self.cur.execute(insert_sql, uid)
            self.conn.commit()
            logging.info(f'插入失败记录完成 uid:{uid}')
        except pymysql.Error as e:
            logging.error(f'bili_user_fail数据写入数据库异常 {e}')
