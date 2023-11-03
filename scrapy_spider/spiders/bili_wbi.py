# encoding: utf-8
# @Time : 2023/11/2 17:06
# @Auther : ISLEY
# @File : bili_wbi.py
# @DESC : b站wbi签名算法
import logging
from functools import reduce
from hashlib import md5
import urllib.parse
import time
from datetime import datetime
import requests
import random

"""
    b站api接口wbi验证 
    具体文档参考 https://github.com/SocialSisterYi/bilibili-API-collect/blob/master/docs/misc/sign/wbi.md
    简单讲:
        api接口需带两个参数w_rid 和 wts  
            #不过有时候抽风, 不带能也爬 , 带了更容易
            getWbiKeys() 方法获取最开始两个token 与用户和ip无关, 全站统一 , 每日刷新
                https://api.bilibili.com/x/web-interface/nav 接口获得
            之后经过一系列加密 通过请求参数生成w_rid , wts
        
        使用  
            本地爬第一次getWbiKeys() 记住即可
                服务器不停爬 需要变更日期时 重新访问一次getWbiKeys() 
            之后每个请求需要通过encWbi() 增加w_rid和wts参数即可
"""


def _get_mixin_key(orig: str):
    """对 imgKey 和 subKey 进行字符顺序打乱编码"""
    mixin_key_enc_tab = [
        46, 47, 18, 2, 53, 8, 23, 32, 15, 50, 10, 31, 58, 3, 45, 35, 27, 43, 5, 49,
        33, 9, 42, 19, 29, 28, 14, 39, 12, 38, 41, 13, 37, 48, 7, 16, 24, 55, 40,
        61, 26, 17, 0, 1, 60, 51, 30, 4, 22, 25, 54, 21, 56, 59, 6, 63, 57, 62, 11,
        36, 20, 34, 44, 52
    ]
    return reduce(lambda s, i: s + orig[i], mixin_key_enc_tab, '')[:32]


def _enc_wbi(params: dict, img_key: str, sub_key: str, ):
    """为请求参数进行 wbi 签名"""
    mixin_key = _get_mixin_key(img_key + sub_key)
    curr_time = round(time.time())
    params['wts'] = curr_time  # 添加 wts 字段
    params = dict(sorted(params.items()))  # 按照 key 重排参数
    # 过滤 value 中的 "!'()*" 字符
    params = {
        k: ''.join(filter(lambda chr: chr not in "!'()*", str(v)))
        for k, v
        in params.items()
    }
    query = urllib.parse.urlencode(params)  # 序列化参数
    wbi_sign = md5((query + mixin_key).encode()).hexdigest()  # 计算 w_rid
    params['w_rid'] = wbi_sign
    return params


def _get_wbi_keys() -> tuple[str, str]:
    """获取最新的 img_key 和 sub_key"""
    resp = requests.get('https://api.bilibili.com/x/web-interface/nav')
    resp.raise_for_status()
    json_content = resp.json()
    img_url: str = json_content['data']['wbi_img']['img_url']
    sub_url: str = json_content['data']['wbi_img']['sub_url']
    img_key = img_url.rsplit('/', 1)[1].split('.')[0]
    sub_key = sub_url.rsplit('/', 1)[1].split('.')[0]
    logging.info(f'获取img_key: {img_key} , sub_key: {sub_key}')
    return img_key, sub_key


"""
    通过请求获取buvid3 和 buvid4
"""


def _get_cookie_buvid() -> tuple[str, str]:
    """获取游客buvid3 和 buvid4"""
    resp = requests.get("https://api.bilibili.com/x/frontend/finger/spi")
    resp.raise_for_status()
    json_content = resp.json()
    buvid3: str = json_content['data']['b_3']
    buvid4: str = json_content['data']['b_4']
    logging.info(f"获取buvid3: {buvid3} , buvid4: {buvid4}")
    return buvid3, buvid4


def get_buvid3():
    buvid3, buvid4 = _get_cookie_buvid()
    return buvid3


"""
    通过js逆向获得buvid3 耗时可忽略 非常快
"""


def gen_buvid3():
    e = a(8)
    t = a(4)
    r = a(4)
    n = a(4)
    o = a(12)
    i = int(time.time() * 1000)
    return f"{e}-{t}-{r}-{n}-{o}{s(str(i % 100000), 5)}infoc"


def a(e):
    t = ""
    for _ in range(e):
        t += o(16 * random.random())
    return s(t, e)


def o(e):
    return format(int(e), 'X')


def s(e, t):
    r = ""
    if len(e) < t:
        for _ in range(t - len(e)):
            r += "0"
    return r + e


class BiliWbi:
    def __init__(self):
        self.img_key, self.sub_key = _get_wbi_keys()

    def get_wbi(self, params: dict):
        signed_params = _enc_wbi(params=params, img_key=self.img_key, sub_key=self.sub_key)
        query = urllib.parse.urlencode(signed_params)
        return query


if __name__ == '__main__':
    # bili_wbi = BiliWbi()
    # query = bili_wbi.get_wbi({'mid': 83})
    # print(query)
    start_time = datetime.now()
    print(gen_buvid3())
    end_time = datetime.now()
    print(end_time - start_time)
