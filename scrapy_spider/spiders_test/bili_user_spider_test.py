# encoding: utf-8
# @Time : 2023/11/1 19:18
# @Auther : ISLEY
# @File : bili_user_spider_test.py
# @DESC :

import scrapy_spider.utils.pathutil as pathutil
from pathlib import Path
from scrapy.http import HtmlResponse
from scrapy_spider.spiders.bili_user_spider import BiliUserSpider
from scrapy_spider.pipelines import BiliUsersSavePipeline
from fake_useragent import UserAgent


def test_parse():
    # 获取本地html文件 用于测试
    filename = pathutil.get_abs_path('local_html/bili_user_test.json')
    content = Path(filename).read_text(encoding='utf-8')

    print(content)

    # 创建spider对象
    spider = BiliUserSpider()

    # 手动创建响应
    response = HtmlResponse(url=filename, body=content, encoding='utf-8')
    infos = spider.parse(response)
    for info in infos:
        print(info)
        yield info


def test_save():
    pipeline = BiliUsersSavePipeline()
    for item in test_parse():
        pipeline.process_item(item=item, spider=None)

    pipeline.close_spider(None)


def test_gen_request():
    user_agent = UserAgent()
    for uid in range(1, 10):
        url = f'https://api.bilibili.com/x/space/wbi/acc/info?mid={uid}'
        headers = {
            "User-Agent": user_agent.chrome,
            "Referer": f"https://space.bilibili.com/{uid}/"
        }
        print(url)
        print(headers)


if __name__ == '__main__':
    test_parse()
    # test_save()
    # test_gen_request()
