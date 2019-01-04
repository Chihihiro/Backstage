# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 22:17
# @Author  : 逗比i
# @Project : Backstage
# @File    : 点容宝.py
# @Software: PyCharm
# @Describe:

from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep
import json
import time


class DRB(BaseSpider):
    def __init__(self, account):
        super(DRB, self).__init__(account)

    def get_info(self):
        # 设置session
        session = Session()
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
            "accessToken": "88f29e20c200b264e367411149765fc7",
            "Origin": "http://xayjy.zaixianjieshu.com",
            "Referer": "http://xayjy.zaixianjieshu.com/xayjy/H5/flowAdmin/index.html",
            "Content-Type": "application/json; charset=utf-8"
        }
        # 页面url
        json_url = "http://47.110.185.92:88/channel/admin/data"
        args = {
            'channelCode': "",
            'merchantId': "0",
            'registerBeginDate': int(time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S")))*1000,
            'registerEndDate': int(time.mktime(time.strptime(f"{self.tomorrow} 00:00:00", "%Y-%m-%d %H:%M:%S")))*1000
        }
        # 请求url
        response = session.post(json_url, headers=headers, json=args)
        # info = response.json()
        # print(info)
        info = response.json()['data']['channelDataList'][0]
        # 获取结果
        print(info)
        result = {
            "注册人数": info['registerCount'],
            "实名人数": "null",
            "申请人数": info['applyCount'],
            "放款人数": info['agreeCount']
        }
        print(result)
        self.write_sql(result)


SH = {
    "login_url": 'http://xayjy.zaixianjieshu.com/xayjy/H5/flowAdmin/index.html#/user/login',
    "area": "上海",
    "product": "易借钱包",
    "username": "ht12",
    "password": "12345",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(1200)













