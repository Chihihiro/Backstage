#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/22 0022 11:13 
# @Author : Chihiro 
# @Site :  
# @File : 葫芦钱包.py 
# @Software: PyCharm





from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep
import json


class XHY(BaseSpider):
    def __init__(self, account):
        super(XHY, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="userName"]',
            "password": '//*[@id="password"]',
            "login_button": '//*[@id="doLogin"]',
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.no_check_get_cookie(xpath_info)
        # 将cookie设置给session
        print(cookie_to_dict(cookie))
        session.cookies.update(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        url = f"http://hlqb.k39120.cn/customer/channelUser/getData?page=1&limit=10&channelId=&customerProvince=&createTimeStart={self.today}&createTimeEnd={self.today}&infoLevel="
        # 请求url
        response = session.get(url, headers=headers)
        # 构造Selector
        info = response.json()['count']
        print(info)
        # 获取结果
        result = {
            "注册人数": info,
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            '备注': ''
        }
        self.write_sql(result)


SH = {
    "login_url": "http://hlqb.k39120.cn/login",
    "area": "",
    "product": "葫芦钱包",
    "username": "fu17",
    "password": "Aa123456",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        XHY(each).get_info()
        sleep(600)