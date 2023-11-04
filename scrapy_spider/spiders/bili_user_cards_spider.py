# encoding: utf-8
# @Time : 2023/11/4 14:41
# @Auther : ISLEY
# @File : bili_user_cards_spider.py
# @DESC :
"""
    通过cards接口批量获取用户信息
        api说明参考 bili_user_readme.md
            该接口直接从别人文档里找到的, 具体入口未知

        测试 理想情况:
            单ip
                每条请求20个uid  5w条数据/min 实际请求数约2200/min
                每条请求50个uid  也5w/min左右 实际请求数约800/min
                如果没被禁ip, 瓶颈在items处理上 大概4-5w/min
            PS:
                体感上50uid每条失败率更高? 容易返回值600003
                20uid 约触发600003响应10-20次, 即丢失200-400数据/ 10w条数据

"""
import json
import logging
import datetime
from typing import Iterable, Any

import scrapy
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.http import Response
from scrapy_spider.items import BiliUserItem


def _datetime_format(local_timestamp):
    # 默认值 1970 01 01 00 00 01
    local_time = datetime.datetime.fromtimestamp(1)
    length = len(str(local_timestamp))
    if length == 10:
        # 秒单位时间戳
        local_timestamp = int(local_timestamp)
        if local_timestamp < 0:
            local_time = datetime.datetime.fromtimestamp(0) + datetime.timedelta(seconds=-639129600)
    elif length == 13:
        # 毫秒单位时间戳
        local_time = datetime.datetime.fromtimestamp(int(local_timestamp) / 1000)

    return local_time.strftime("%Y-%m-%d %H:%M:%S")


class BiliUserCardsSpider(scrapy.Spider):
    name = 'bili_user_cards'
    custom_settings = {
        # "DOWNLOAD_DELAY": "0.04",  # 请求延迟 可以为小数
        "CONCURRENT_REQUESTS": "16",  # 最大并发数 默认16
        "CONCURRENT_REQUESTS_PER_DOMAIN": "8",  # 最大单域名并发数 默认8
        "ITEM_PIPELINES": {
            "scrapy_spider.pipelines.BiliUsersSavePipeline": 300
        }
    }

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self.error_count = 0

    def start_requests(self) -> Iterable[Request]:
        start_uid = 1700000  # 初始uid
        end_uid = start_uid + 100000  # 终止uid 不包含
        uids_len = 20  # 每条请求获取多少用户, 最大50
        uids_arr = []
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }
        for uid in range(start_uid, end_uid):
            uids_arr.append(str(uid))
            if len(uids_arr) == uids_len:
                uids = ','.join(uids_arr)
                url = f"https://api.vc.bilibili.com/account/v1/user/cards?uids={uids}"
                yield scrapy.Request(url=url, headers=headers, callback=self.parse, cb_kwargs={'uids_arr': uids_arr})

                uids_arr = []

    def parse(self, response: Response, uids_arr) -> Any:
        try:
            response_json = json.loads(response.text)
            code = response_json['code']
            message = response_json['message']
            if code == 0:
                data_list = response_json['data']
                for json_data in data_list:
                    try:
                        name = str(json_data['name'])
                        if name.isspace() or len(name.strip()) == 0:
                            # 用户不存在直接跳过
                            continue

                        item = BiliUserItem()
                        # 基本信息
                        item['uid'] = json_data['mid']
                        item['name'] = name
                        item['sex'] = json_data['sex']
                        item['face'] = json_data['face']
                        item['sign'] = json_data['sign']
                        item['rank'] = json_data['rank']
                        item['level'] = json_data['level']
                        item['jointime'] = _datetime_format(0)
                        item['coins'] = 0
                        item['birthday'] = _datetime_format(json_data['birthday'])

                        # 会员信息
                        vip = json_data['vip']
                        item['vip_type'] = vip['type']
                        item['vip_status'] = vip['status']
                        item['vip_due_date'] = _datetime_format(vip['due_date'])
                        item['vip_label'] = vip['label']['text']

                        # 认证信息
                        official = json_data['official']
                        item['official_role'] = official['role']
                        item['official_title'] = official['title']
                        item['official_desc'] = official['desc']
                        item['official_type'] = official['type']

                        # 爬取成功
                        item['crawl_status'] = True
                        yield item

                    except Exception as e:
                        logging.error(f"数据解析异常 {e} , data: {json_data}")
                        item = BiliUserItem()
                        item['uid'] = json_data['mid']
                        item['crawl_status'] = False
                        yield item
            else:
                # code > 0 的情况 600006 参数错误, 600007 uid过多等
                # code < 0 的情况 -400 请求错误等
                logging.warning(f"{message} : response: {response_json}")
                logging.warning(f"{message} : url: {response.url}")
                for uid in uids_arr:
                    item = BiliUserItem()
                    item['uid'] = uid
                    item['crawl_status'] = False
                    yield item

        except Exception as e:
            # logging.error(f'响应解析异常 : {e} , {response.url} , {response.text}')
            logging.error(f'未知异常 : {e}')
            self.error_count += 1
        finally:
            if self.error_count >= 10:
                logging.warning(f'异常次数 {self.error_count}')
                raise CloseSpider('异常过多 终止爬虫')
