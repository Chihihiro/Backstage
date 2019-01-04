#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/3 0003 12:40 
# @Author : Chihiro 
# @Site :  
# @File : 花猫.py 
# @Software: PyCharm


import requests
from scrapy import Selector
from BaseSpider import BaseSpider
from requests import Session
from time import sleep


class XHY(BaseSpider):
    def __init__(self, account):
        super(XHY, self).__init__(account)

    def get_info(self):
        session = Session()
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        page_url = "http://huamao.hztiantu.cn/jm-masterv2server/static/userstatlists?channelpwd=12616f6bb6cc873fe4fd3daba6585f7d"

        # 请求url
        response = session.get(page_url, headers=headers)
        # 构造Selector
        data = Selector(text=response.text)
        register = data.xpath('/html/body/div/table/tbody/tr/td[4]/text()').extract()[0]
        # 获取结果
        result = {
            "注册人数": register,
            "实名人数": 'null',
            "申请人数": 'null',
            "放款人数": "null"
        }
        self.write_sql(result)


WD = {
    "login_url": "http://huamao.hztiantu.cn/jm-masterv2server/static/userstatlists?channelpwd=12616f6bb6cc873fe4fd3daba6585f7d",
    "area": "外地",
    "product": "花猫",
    "username": "",
    "password": "",
    "channel": ""
}

all_area = [WD]

for each in all_area:
    XHY(each).get_info()
    sleep(1200)
