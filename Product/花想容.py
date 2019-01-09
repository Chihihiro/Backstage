#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/9 0009 15:42 
# @Author : Chihiro 
# @Site :  
# @File : 花想容.py 
# @Software: PyCharm


from selenium import webdriver
from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
import json
from time import sleep
import time

class BJZ(BaseSpider):
    def __init__(self, account):
        super(BJZ, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="user"]',
            "password": '//*[@id="pwd"]',
            "login_button": '//*[@id="sub"]',
            "check_code": "",
            "code_image_url": "",
            "success_ele": ""
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.no_check_get_cookie(xpath_info)
        # 给session设置cookie
        session.cookies.update(cookie_to_dict(cookie))
        print(cookie_to_dict(cookie))
        # json的url
        url = "http://de-hxr.91yiyongbao.com/selectClientTime"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        arg = {
            'page': 1,
            'statetime': f"{self.today} 00:00:00",
            'endtime': f"{self.tomorrow} 00:00:00",
        }

        # 访问url
        response = session.post(url, headers=headers, data=arg)
        json_info = response.json()
        print(json_info)

        result = {
            "注册人数": json_info["linenumber"],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": ""
        }
        self.write_sql(result)


SH = {
    "login_url": "http://de-hxr.91yiyongbao.com/clientlogin.html",
    "area": "",
    "product": "花想容",
    "username": "婷113",
    "password": "123456",
    "channel": ""
}


all_local = [SH]
while True:
    for each_local in all_local:
        spider = BJZ(each_local)
        spider.get_info()
    time.sleep(1200)
