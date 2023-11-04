# encoding: utf-8
# @Time : 2023/10/29 23:50
# @Auther : ISLEY
# @File : py_test.py
# @DESC : python函数测试
import datetime
import time
import uuid

"""
    range 左闭右开
"""


def range_test():
    for i in range(2, 10):
        print(i, end=',')


def time_test():
    # print(len(str(1726934400000)))
    print(len(str(-639129600)))
    # local_time = datetime.datetime.fromtimestamp(0) + datetime.timedelta(seconds=-639129600)
    local_time = datetime.datetime.fromtimestamp(1726934400)
    print(local_time.strftime("%Y-%m-%d %H:%M:%S"))


def uuid_test():
    print(uuid.uuid4())


def empty_test():
    str = " "
    str2 = ""
    print(str.isspace())  # 只包含空格为True , 空/其他字符串为False
    print(str2.isspace())
    print(len(str))
    print(len(str2))
    print(len(str.strip()))  # 去前后空格后判断长度


def join_test():
    start_uid = 1098500
    end_uid = start_uid + 10000
    uids_len = 50
    uids_arr = []
    for uid in range(start_uid, end_uid):
        uids_arr.append(str(uid))
        if len(uids_arr) == uids_len:
            uids = ','.join(uids_arr)
            url = f"https://api.vc.bilibili.com/account/v1/user/cards?uids={uids}"
            uids_arr = []
            print(url)

def split_test():
    uids = "361090,361091,361092,361093,361094,361095,361096,361097,361098,361099,361100,361101,361102,361103,361104,361105,361106,361107,361108,361109"
    for uid in uids.split(","):
        print(uid)

if __name__ == '__main__':
    # range_test()
    # time_test()
    # uuid_test()
    # empty_test()
    join_test()
    # split_test()