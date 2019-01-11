#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/10 0010 16:43 
# @Author : Chihiro 
# @Site :  
# @File : 阿壹钱包.py 
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
            "username": '//*[@id="name"]',
            "password": '//*[@id="password"]',
            "login_button": '//*[@id="submitButton"]',
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
        url = "http://www.ayiqianbao.com/ayipal/manager/member/statisticExtendMember.do"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }

        arg = {

            'recMobile': '',
            'lockStatus': 'NORMAL',
            'blacklist': 0,
            'type': 'allMember',
            'startDate': f"{self.today}",
            'endDate': f"{self.today}",
            'limit': 10,
            'start': 0,
        }
        # 访问url

        response = session.post(url, headers=headers, json=arg)
        info = response.json()['rows'][0]
        print(info)

        result = {
            "注册人数": info['memberCount'],
            "实名人数": info['auditPassCount'],
            "申请人数": "null",
            "放款人数": "null",
            "备注": '68个余量'

        }
        self.write_sql(result)


SH = {
    "login_url": 'http://www.ayiqianbao.com/ayipal/manager/logout.do',
    "area": "",
    "product": "阿壹钱包",
    "username": "lin01",
    "password": "123456",
    "channel": ""
}


all_local = [SH]


while True:
    for each in all_local:
        BJZ(each).get_info()
    time.sleep(1200)
