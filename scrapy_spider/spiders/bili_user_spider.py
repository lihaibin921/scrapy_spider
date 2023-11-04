# encoding: utf-8
# @Time : 2023/11/1 15:19
# @Auther : ISLEY
# @File : bili_user_spider.py
# @DESC :
"""
    b站用户信息爬取
        api说明查看 bili_user_readme.md
            接口获取的buvid3 缺点太多 , 逆向了js  bw.gen_buvid3()
                # 几乎不耗时, 每个request可以分配不同的buvid3
            执行结果
                单ip 并发8
                    第一次 5000条测试 覆盖率99.6% 速度3500/min # 未成功0.4%为账户注销的用户
                    第二次 5000条 成功率50%左右 速度1500/min
        PS:
            无论是ua , cookie等都只是验证手段, 最终是否封禁还是看ip访问频率 , 有个ip池子会大大提高效率
            反爬机制(大概):
                大概是5min请求数计算, 据说150左右(我靠, 这也太低了)
                惩罚: 对ip进行的限流 限流时间大约30min
                    限流期间50%请求通过, 50%请求非法 , 降速也无效
                    怎么实现的?
                        猜测:
                            1 常用的 计数器, 窗口, 令牌桶, 漏筒桶 都不太像
                            2 nginx? 分布式一部分机器拒绝, 一部分通过?
                            3 难不成就真的做了个概率限流吧?
                另外
                    cookie中携带SESSDATA 字段, 即登录用户, 限流算法有变 , 访问量放宽


"""
from typing import Any
import scrapy
from scrapy.exceptions import CloseSpider
import logging
import json
import time
from scrapy_spider.items import BiliUserItem
import scrapy_spider.spiders.bili_wbi as bw


def _time_format(local_timestamp):
    length = len(str(local_timestamp))
    if length == 10:
        # 秒单位时间戳
        local_timestamp = int(local_timestamp)
    elif length == 13:
        # 毫秒单位时间戳
        local_timestamp = int(local_timestamp) / 1000
    else:
        # 默认值 1 , mysql不允许插入零点时间
        local_timestamp = 1

    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(local_timestamp))


class BiliUserSpider(scrapy.Spider):
    name = 'bili_user'
    allowed_domains = ['api.bilibili.com']
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
        self.error_count = 0  # 失败次数过多时 用来终止爬虫

    def start_requests(self):
        bili_wbi = bw.BiliWbi()
        start_uid = 111142  # 初始uid 需手动更改
        end_uid = start_uid + 10000  # 截止uid 不包含
        for uid in range(start_uid, end_uid):
            # 增加wbi加密字段 关键校验字段
            query = bili_wbi.get_wbi({"mid": uid})
            url = f'https://api.bilibili.com/x/space/wbi/acc/info?{query}'
            # headers 可能不需要, 但是UA属性非法则会报错
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
                "Referer": f"https://space.bilibili.com/{uid}"
            }
            # buvid3 在爬取速度较高的情况下会被验证
            cookies = {
                'buvid3': bw.gen_buvid3()
            }
            # 注意cb_kwargs 显示的传递uid给parse方法
            yield scrapy.Request(url=url, headers=headers, cookies=cookies, callback=self.parse, cb_kwargs={'uid': uid})

    def parse(self, response, uid):
        try:
            response_json = json.loads(response.text)
            code = response_json['code']
            if code == 0:
                # 正确获取数据 创建item对象
                if 'data' in response_json.keys():
                    json_data = response_json['data']

                    item = BiliUserItem()
                    # 基本信息
                    item['uid'] = json_data['mid']
                    item['name'] = json_data['name']
                    item['sex'] = json_data['sex']
                    item['face'] = json_data['face']
                    item['sign'] = json_data['sign']
                    item['rank'] = json_data['rank']
                    item['level'] = json_data['level']
                    item['jointime'] = _time_format(json_data['jointime'])
                    item['coins'] = json_data['coins']
                    item['birthday'] = json_data['birthday']

                    # 会员信息
                    vip = json_data['vip']
                    item['vip_type'] = vip['type']
                    item['vip_status'] = vip['status']
                    item['vip_due_date'] = _time_format(vip['due_date'])
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
            elif code == -401:
                # 被判定为爬虫
                error_desc = response_json['data']['ga_data']['decisions']
                logging.warning(
                    f"非法请求: uid:{uid} , desc:{error_desc}")

                # 失败直接存库, 之后再重爬
                item = BiliUserItem()
                item['uid'] = uid
                item['crawl_status'] = False
                yield item

            else:
                # 其余情况 -403无权限 -404账户不存在等
                logging.warning(f"无效uid: {uid} ,response: {response_json}")

        except Exception as e:
            logging.error(f'响应解析异常 : {e} , {response.url} , {response.text}')
            self.error_count += 1
        finally:
            # 异常次数10次 直接终止
            if self.error_count >= 10:
                logging.warning(f'异常次数 {self.error_count}')
                raise CloseSpider('异常过多 终止爬虫')
