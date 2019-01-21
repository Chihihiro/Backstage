#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/10 0010 13:28 
# @Author : Chihiro 
# @Site :  
# @File : 周转侠.py
# @Software: PyCharm



from BaseSpider import BaseSpider
from time import sleep
from requests import Session
from scrapy import Selector
import re

class XHY(BaseSpider):
    def __init__(self, account):
        super(XHY, self).__init__(account)

    def get_info(self):
        # 设置session
        session = Session()
        # 获取cookie
        # json的url
        url = 'http://yuehuixinxi.com/third_spreads/?token=fba3b33f205e6407880799168534c72ef3b7272b9ecc90f3e9dae088e6aa1286'
        # 设置session
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        response = session.get(url, headers=headers)
        # 构造Selector
        info = Selector(text=response.text)
        # print()
        a = info.xpath('//*[@id="format_canal_register_feedback"]/text()').re('(\d+)')[0]

        # 获取结果
        result = {
            "注册人数": a,
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": ''
        }
        self.write_sql(result)


WD = {
    "login_url": "",
    "area": "",
    "product": "周转侠",
    "username": "",
    "password": "",
    "channel": ""
}

all_local = [WD]

while True:
    for each_local in all_local:
        spider = XHY(each_local)
        spider.get_info()
    sleep(600)













