# encoding: utf-8
# @Time : 2023/10/29 23:50
# @Auther : ISLEY
# @File : py_test.py
# @DESC : python函数测试
import time
import uuid

"""
    range 左闭右开
"""


def range_test():
    for i in range(2, 10):
        print(i, end=',')


def time_test():
    print(len(str(1726934400000)))
    local_time = time.localtime(1726934400000)
    print(time.strftime("%Y-%m-%d %H:%M:%S", local_time))


def uuid_test():
    print(uuid.uuid4())


if __name__ == '__main__':
    # range_test()
    # time_test()
    uuid_test()
