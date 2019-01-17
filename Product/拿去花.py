#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/16 0016 11:11 
# @Author : Chihiro 
# @Site :  
# @File : 拿去花.py 
# @Software: PyCharm



import re
from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
import time
import warnings
from scrapy import Selector
import json


class BJZ(BaseSpider):
    def __init__(self, account):
        super(BJZ, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="userId"]',
            "password": '//*[@id="password"]',
            "login_button": '//*[@id="login"]',
            "check_code": "",
            "code_image_url": "",
            "success_ele": ""
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.no_check_get_cookie(xpath_info)
        print(cookie)
        # 给session设置cookie
        session.cookies.update(cookie_to_dict(cookie))
        # json的url
        url = "http://demand.lianfen360.com/market?id=mk103BP3r&login=true"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 访问url

        response = session.get(url, headers=headers)
        selector = Selector(text=response.text).xpath('/html/body/div/div[6]/div/h2/text()')
        print(selector)

        result = {
            "注册人数": selector.re('注册数:(\d+)')[0],
            "实名人数": "null",
            "申请人数": selector.re('申请数:(\d+)')[0],
            "放款人数": "null",
            "备注": ''

        }
        self.write_sql(result)


SH = {
    "login_url": 'http://demand.lianfen360.com/market?id=mk103BP3r',
    "area": "",
    "product": "拿去花",
    "username": "mk103BP3r",
    "password": "123456",
    "channel": ""
}


all_local = [SH]


while True:
    for each in all_local:
        BJZ(each).get_info()
    time.sleep(1200)
