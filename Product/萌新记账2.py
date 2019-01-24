#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/23 0023 11:26 
# @Author : Chihiro 
# @Site :  
# @File : 萌新记账2.py 
# @Software: PyCharm







from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep
import json
import re

class XHY(BaseSpider):
    def __init__(self, account):
        super(XHY, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="username"]',
            "password": '//*[@id="pwd"]',
            "login_button": '//*[@id="Form1"]/button',
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.no_check_get_cookie(xpath_info)
        # 将cookie设置给session
        session.cookies.update(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        url = f"http://mxqb.1wgk83.cn/index.php/Order/log.html?start_time={self.today}&end_time={self.today}"
        # 请求url
        response = session.get(url, headers=headers)
        # 构造Selector
        html = Selector(text=response.text)
        # 获取结果
        info = html.xpath('/html/body/div/div/div/div/div[2]/table/tfoot/tr/td/ul/li/a/text()').extract()[0]
        num = re.search('共(.+?)条', info).group(1)
        result = {
            "注册人数": num,
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            '备注': ''
        }
        self.write_sql(result)


SH = {
    "login_url": "http://mxqb.1wgk83.cn/Login/index.html",
    "area": "",
    "product": "萌新记账-安徽",
    "username": "mxklsq",
    "password": "123456",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        XHY(each).get_info()
        sleep(600)