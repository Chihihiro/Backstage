#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/11 0011 16:56 
# @Author : Chihiro 
# @Site :  
# @File : 往来金融.py 
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
            "username": '/html/body/div/div/form/div[2]/div[2]/input',
            "password": '/html/body/div/div/form/div[2]/div[3]/input',
            "login_button": '/html/body/div/div/form/div[2]/div[4]/button',
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
        url = "http://www.91yiyongbao.com/selectClientTime"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }

        arg = {

            'page': 1,
            'statetime': f"{self.today}"+ " 00:00:00",
            'endtime': f"{self.tomorrow}"+ " 00:00:00"

        }
        # 访问url

        response = session.post(url, headers=headers, data=arg)
        info = response.json()

        result = {
            "注册人数": info['linenumber'],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": ''

        }
        self.write_sql(result)


SH = {
    "login_url": 'http://www.91yiyongbao.com/Clientlogin',
    "area": "",
    "product": "往来金融",
    "username": "往唯有一",
    "password": "123456",
    "channel": ""
}


all_local = [SH]


while True:
    for each in all_local:
        BJZ(each).get_info()
    time.sleep(1200)
