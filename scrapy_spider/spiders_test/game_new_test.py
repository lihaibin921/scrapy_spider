# encoding: utf-8
# @Time : 2023/10/30 15:54
# @Auther : ISLEY
# @File : game_new_test.py
# @DESC :


from scrapy.http import HtmlResponse
from pathlib import Path
import scrapy_spider.utils.pathutil as pathutil
from scrapy_spider.spiders.game_new_spider import GameSpider
import pandas as pd


def test_parse():
    # 获取本地html文件 用于测试
    filename = pathutil.get_abs_path('local_html/game_new.html')
    content = Path(filename).read_text(encoding='utf-8')

    # 创建GameSpider对象
    spider = GameSpider()

    # 手动创建Response 并测试解析逻辑
    response = HtmlResponse(url=filename, body=content, encoding='utf-8')
    for game in spider.parse(response):
        yield game


if __name__ == '__main__':
    data_list = []
    for item in test_parse():
        data_list.append(item)
        if len(data_list) == 10:
            break

    df = pd.DataFrame(data_list)
    df.to_csv("data.csv", index=False, sep=',', mode='a', header=False)

    print(df)
