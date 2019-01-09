#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/9 0009 16:08 
# @Author : Chihiro 
# @Site :  
# @File : 富二贷.py 
# @Software: PyCharm




from selenium import webdriver
from scrapy import Selector
from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
import json
from time import sleep
import time
import re

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
        # 给session设置cookie
        session.cookies.update(cookie_to_dict(cookie))
        print(cookie_to_dict(cookie))
        # json的url
        url = "http://demand.lianfen360.com/market?id=mk92rXg2&login=true"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }


        # 访问url
        response = session.get(url, headers=headers)
        info = Selector(text=response.text)
        index = info.xpath('/html/body/div/div[6]/div/h2/text()').extract()[0]
        print(index)

        result = {
            "注册人数": re.search("注册数:(.+?);", index).group(1),
            "实名人数": "null",
            "申请人数": re.search("申请数:(.+?);", index).group(1),
            "放款人数": "null",
            "备注": ""
        }
        self.write_sql(result)


SH = {
    "login_url": "http://demand.lianfen360.com/market?id=mk92rXg2",
    "area": "",
    "product": "富二贷",
    "username": "mk92rXg2",
    "password": "123456",
    "channel": ""
}


all_local = [SH]
while True:
    for each_local in all_local:
        spider = BJZ(each_local)
        spider.get_info()
    time.sleep(1200)
