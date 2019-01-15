#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/15 0015 12:28 
# @Author : Chihiro 
# @Site :  
# @File : 融小鱼.py 
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
            "username": '/html/body/div/div[2]/form/div[1]/input',
            "password": '/html/body/div/div[2]/form/div[2]/input',
            "login_button": '/html/body/div/div[2]/form/div[3]/div[2]/button',
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
        url = f"http://report.xdy7.com/user/leads/daily?source={self.channel}&datebegin={self.today}&dateend={self.today}"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }

        # 访问url

        response = session.get(url, headers=headers)
        info = Selector(text=response.text)

        result = {
            "注册人数": info.xpath('//table//tr/td[2]/text()').extract()[0],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": ''

        }
        self.write_sql(result)


SH = {
    "login_url": 'http://report.xdy7.com/auth/login',
    "area": "",
    "product": "融小鱼",
    "username": "1890000037",
    "password": "qwer1234",
    "channel": "612"
}


all_local = [SH]


while True:
    for each in all_local:
        BJZ(each).get_info()
    time.sleep(1200)
