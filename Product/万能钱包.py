#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/7 0007 18:09 
# @Author : Chihiro 
# @Site :  
# @File : 万能钱包.py 
# @Software: PyCharm




from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep
import time

class XHY(BaseSpider):
    def __init__(self, account):
        super(XHY, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="account"]',
            "password": '//*[@id="password"]',
            "login_button": '/html/body/div/div/div/form/div[4]',
            "check_code": '//*[@id="captcha"]',
            "code_image_url": '//*[@id="validateCodeImg"]',
            "success_ele": '/html/body/div/div[1]/div[2]/ul/li[1]/a'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (504, 492, 635, 535), "10400")
        # 将cookie设置给session
        session.cookies.update(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        page_url = f"http://partner.ytrong.com/partner/info?id=354&page=1&limit=30"
        # 请求url
        response = session.get(page_url, headers=headers)
        # 构造Selector
        data = response.json()['rows'][0]
        print(data)


        # 获取结果
        result = {
            "注册人数": data['userCount'],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null"
        }
        self.write_sql(result)
        print(result)


SH = {
    "login_url": "http://partner.ytrong.com/partner/login",
    "area": "上海",
    "product": "万能钱包",
    "username": "mlh1220",
    "password": "456123",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        XHY(each).get_info()
        sleep(1200)