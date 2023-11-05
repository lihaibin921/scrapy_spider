# encoding: utf-8
# @Time : 2023/11/5 17:46
# @Auther : ISLEY
# @File : bili_user_follow_spider.py
# @DESC :
"""
    从bili_user库中拿出有效uid数据
    调用https://api.bilibili.com/x/relation/stat?vmid={uid} 获取关注数和粉丝数
    执行批量更改操作 , 修改bili_user中粉丝数量

    该接口几乎无限流 8400/min 没有批量接口 只能uid查还是比较慢
        # 可以考虑先查等级高 / 有认证 / 开会员的都行
"""
import json
import logging
from typing import Iterable, Any

import scrapy
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.http import Response

from scrapy_spider.utils.mysql_util import MysqlDatabase


class BiliUserFollowSpider(scrapy.Spider):
    name = 'bili_user_follow'
    custom_settings = {
        "CONCURRENT_REQUESTS": "16",  # 最大并发数 默认16
        "CONCURRENT_REQUESTS_PER_DOMAIN": "8"  # 最大单域名并发数 默认8
    }

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.db = MysqlDatabase()
        self.error_count = 0
        self.update_arr = []

    def start_requests(self) -> Iterable[Request]:

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }
        # 从本地表拿uid
        uids_sql = 'SELECT uid FROM bili_user WHERE uid >%s AND `level` = 6 ORDER BY uid  LIMIT %s'
        start_uid = 2400825  # 最小uid 不包含
        limit_num = 200  # 本地库一次取出uid的次数
        total_num = 0  # 总爬取数, 用来终止程序
        while total_num < 1000000:
            result = self.db.execute_query(uids_sql, params=(start_uid, limit_num))
            # result 结构: ((1,), (2,), (3,)...)
            if len(result) > 0:
                for data in result:
                    url = f'https://api.bilibili.com/x/relation/stat?vmid={data[0]}'
                    yield scrapy.Request(url=url, headers=headers, callback=self.parse)
                start_uid = result[-1][0]
                total_num += len(result)
            else:
                break

    def parse(self, response: Response, **kwargs: Any) -> Any:
        try:
            response_json = json.loads(response.text)
            code = response_json['code']
            message = response_json['message']

            if code == 0:
                data = response_json['data']
                uid = data['mid']
                following = int(data['following'])
                follower = int(data['follower'])

                # 懒着按scrapy框架写了, 直接存库
                params = (following, follower, uid)
                self.update_arr.append(params)
                if len(self.update_arr) >= 200:
                    self._update_datas(self.update_arr)
                    self.update_arr = []
                    logging.info(f'批量更改粉丝数完成')

                logging.info(f'uid: {uid} , 关注数: {following} , 粉丝数: {follower}')
            else:
                logging.warning(f"{message} : url: {response.url}")
        except Exception as e:
            logging.error(f'未知异常 : {e}')
            self.error_count += 1
        finally:
            if self.error_count >= 10:
                logging.warning(f'异常次数 {self.error_count}')
                raise CloseSpider('异常过多 终止爬虫')

    def closed(self, reason):
        logging.info("--------执行spider closed方法--------")
        if len(self.update_arr) > 0:
            self._update_datas(self.update_arr)
            logging.info("closed方法: 批量更改粉丝数完成")
        self.db.close_connection()

    def _update_datas(self, datas):
        update_sql = 'UPDATE bili_user SET following = %s , follower = %s WHERE uid = %s'
        self.db.execute_many(update_sql, datas)
