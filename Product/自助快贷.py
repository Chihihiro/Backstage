#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/21 0021 15:04 
# @Author : Chihiro 
# @Site :  
# @File : 自助快贷.py 
# @Software: PyCharm


from requests import Session
from BaseSpider import BaseSpider
from scrapy import Selector
from time import sleep
import json
import time
from DealWithCookie import cookie_to_dict



class DRB(BaseSpider):
    def __init__(self, account):
        super(DRB, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="loginform-username"]',
            "password": '//*[@id="loginform-password"]',
            "login_button": '//*[@id="login-form"]/div/button',
            "check_code": '',
            "code_image_url": '',
            "success_ele": ''
        }
        # 获取cookie
        cookie = self.no_check_get_cookie(xpath_info)

        # 将cookie设置给session
        session = Session()
        # 设置session
        session.cookies.update(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        url = f"https://ssda.xyshuj.com/?start_date={self.today}&end_date={self.today}"
        # 请求url
        response = session.get(url, headers=headers)
        # 获取结果
        html = Selector(text=response.text)
        result = {
            "注册人数": html.xpath('//*[@id="main-content"]/section/section/div[2]/div/div[2]/table//tr[2]/td[3]/text()').extract()[0],
            "实名人数": "null",
            "申请人数": html.xpath('//*[@id="main-content"]/section/section/div[2]/div/div[2]/table//tr[2]/td[4]/text()').extract()[0],
            "放款人数": html.xpath('//*[@id="main-content"]/section/section/div[2]/div/div[2]/table//tr[2]/td[5]/text()').extract[0],
            "备注": ""
        }
        self.write_sql(result)


SH = {
    "login_url": 'https://ssda.xyshuj.com/site/login',
    "area": "",
    "product": "自助快贷",
    "username": "yzbt01",
    "password": "12345678",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(1200)













