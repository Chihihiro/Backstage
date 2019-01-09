#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/8 0008 11:17 
# @Author : Chihiro 
# @Site :  
# @File : 佳品会.py 
# @Software: PyCharm





from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep
import time
import json


class DRB(BaseSpider):
    def __init__(self, account):
        super(DRB, self).__init__(account)


    def get_info(self):
    #     # 设置session
        session = Session()
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
         }
        # 页面url
        page_url = "http://dnf.cx88qb.com:8080/dnfapp/tongji/user/cpa_tj"
        # post参数
        arg = {
            'channel': '087245d197cf493faf0e3156bb27cb19',
            'start_time': f"{self.today}",
            'end_time': f"{self.today}"

        }
        print(arg)
        # 请求url
        # 请求url
        response = session.post(page_url, headers=headers, data=arg)
        # 获取html
        info = response.json()["data"][0]
        print(info)

        # 获取结果
        result = {
            "注册人数": info['level'],
            "实名人数": info['sm'],
            "申请人数": info["apply"],
            "放款人数": info['apply1']
        }
        self.write_sql(result)


SH = {
    "login_url": "",
    "area": "",
    "product": "佳品会",
    "username": "",
    "password": "",
    "channel": ""
}

all_area = [SH]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(1200)
