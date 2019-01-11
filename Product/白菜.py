#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/10 0010 16:18 
# @Author : Chihiro 
# @Site :  
# @File : 白菜.py 
# @Software: PyCharm


import json
from scrapy import Selector
from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep


class DRB(BaseSpider):
    def __init__(self, account):
        super(DRB, self).__init__(account)

    def get_info(self):
        # 设置session
        session = Session()

        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        url = "http://kxhua.hztiantu.cn/jm-masterv2server/static/userstatlists?channelpwd=85540aede300c4ad714794378338fe2b"
        # 请求url
        response = session.get(url, headers=headers)
        # print(response.status_code)
        html = response.text
        info = Selector(text=html)
        # 获取结果
        result = {
            "注册人数": info.xpath('/html/body/div/table//tr/td[4]/text()').extract()[0],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            '备注': ""
        }
        self.write_sql(result)


WD = {
    "login_url": '',
    "area": "",
    "product": "白菜",
    "username": "",
    "password": "",
    "channel": ""
}


all_area = [WD]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(600)