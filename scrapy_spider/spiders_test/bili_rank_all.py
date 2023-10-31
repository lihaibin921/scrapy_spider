# encoding: utf-8
# @Time : 2023/10/31 23:18
# @Auther : ISLEY
# @File : bili_rank_all.py
# @DESC : b站 视频排行榜

from pathlib import Path
import requests
import scrapy_spider.utils.pathutil as pathutil
import json
import pandas as pd

"""
    由于是ajax请求直接获取json , scrapy有点大材小用了
"""

bili_rank_all_url = r"https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all"
headers = {
    "user_agent": r"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}
columns = [
    'vid', '标题', '图片链接', '视频链接', 'up主', 'up主id', '播放数', '评论数'
]
bili_video_pre_url = r"https://www.bilibili.com/video/"


def bili_rank_all_spider_test():
    json_url = pathutil.get_abs_path("local_html/bili_rank_all.json")
    content = Path(json_url).read_text(encoding='utf-8')
    # print(content)
    data_list = json.loads(content)['data']['list']
    for data in data_list:
        yield [
            data['bvid'],  # vid
            data['title'],  # 标题
            data['pic'],  # 图片链接
            bili_video_pre_url + data['bvid'],  # 视频链接
            data['owner']['name'],  # up主姓名
            data['owner']['mid'],  # up主id
            data['stat']['view'],  # 播放数
            data['stat']['danmaku'],  # 评论数
        ]


def bili_rank_all_spider():
    response = requests.get(bili_rank_all_url, headers=headers)
    rank_list = []
    if response.status_code == 200:
        # print(response.text)
        data_list = json.loads(response.text)['data']['list']
        for data in data_list:
            new_data = [
                data['bvid'],  # vid
                data['title'],  # 标题
                data['pic'],  # 图片链接
                bili_video_pre_url + data['bvid'],  # 视频链接
                data['owner']['name'],  # up主姓名
                data['owner']['mid'],  # up主id
                data['stat']['view'],  # 播放数
                data['stat']['danmaku'],  # 评论数
            ]
            rank_list.append(new_data)
            print(new_data)
    else:
        print(f'请求失败 响应码:{response.status_code}')

    # 写csv
    df = pd.DataFrame(data=rank_list, columns=columns)
    bili_rank_data_url = pathutil.get_abs_path('datas/bili/rank.csv')
    df.to_csv(bili_rank_data_url, index=False, sep=',')


if __name__ == '__main__':
    bili_rank_all_spider()

    # for data in bili_rank_all_spider_test():
    #     print(data)
