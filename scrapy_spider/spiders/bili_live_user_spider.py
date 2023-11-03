# encoding: utf-8
# @Time : 2023/11/3 21:22
# @Auther : ISLEY
# @File : bili_live_user_spider.py
# @DESC :
"""
    b站up主信息爬取(曲线救国)
        使用接口https://api.live.bilibili.com/live_user/v1/Master/info 详情查看bili_user_readme.md

        测试结果 :
            优点
                几乎无限流(10w条数据未触发限流)
                提供粉丝数
                粗筛过滤无效uid还挺好用的
            缺点:
                无用户等级, 大会员等信息
"""
from typing import Iterable, Any
from scrapy_spider.items import BiliLiveUserItem
import scrapy
from scrapy import Request
from scrapy.exceptions import CloseSpider
from scrapy.http import Response
import logging
import json


class BiliLiveUserSpider(scrapy.Spider):
    name = "bili_live_user"
    custom_settings = {
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
        start_uid = 351110
        end_uid = start_uid + 10000
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
        }
        for uid in range(start_uid, end_uid):
            url = f'https://api.live.bilibili.com/live_user/v1/Master/info?uid={uid}'

            yield scrapy.Request(url=url, headers=headers, callback=self.parse, cb_kwargs={'uid': uid})

    def parse(self, response: Response, uid) -> Any:

        try:
            response_json = json.loads(response.text)
            code = response_json['code']
            if code == 0:
                # 请求成功, 解析数据
                json_data = response_json['data']

                info = json_data['info']
                uname = str(info['uname'])
                if uname.isspace() or len(uname.strip()) == 0:
                    # 名字为空 表示不存在该用户, 可能是注销的账户
                    logging.warning(f'无效uid:{uid}')
                else:
                    official_verify = info['official_verify']
                    gender = int(info['gender'])

                    item = BiliLiveUserItem()
                    item['uid'] = uid
                    item['name'] = uname
                    item['face'] = info['face']
                    item['follower'] = json_data['follower_num']
                    item['official_type'] = official_verify['type']
                    item['official_desc'] = official_verify['desc']
                    if gender == 0:
                        item['sex'] = '女'
                    elif gender == 1:
                        item['sex'] = '男'
                    else:
                        item['sex'] = '保密'

                    # 爬取成功
                    item['crawl_status'] = True

                    yield item
            else:
                # 其余情况 1 参数错误 , 被限流等
                logging.warning(f"请求失败: {uid} ,response: {response_json}")

                # 存表重爬
                item = BiliLiveUserItem()
                item['uid'] = uid
                item['crawl_status'] = False
                yield item
        except Exception as e:
            logging.error(f'响应解析异常 : {e} , {response.url} , {response.text}')
            self.error_count += 1
        finally:
            if self.error_count >= 10:
                logging.warning(f'异常次数 {self.error_count}')
                raise CloseSpider('异常过多 终止爬虫')
