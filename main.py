# encoding: utf-8
# @Time : 2023/11/4 16:24
# @Auther : ISLEY
# @File : main.py
# @DESC :
"""
    scrapy 主文件
        调用 shell的方式启动
        优点: 可断点DEBUG
"""
from scrapy.cmdline import execute
import sys
import os

if __name__ == '__main__':
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    execute(['scrapy', 'crawl', 'bili_user_cards'])