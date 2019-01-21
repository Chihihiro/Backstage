#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/21 0021 15:16 
# @Author : Chihiro 
# @Site :  
# @File : 锦鲤钱包.py 
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
            "username": '//*[@id="id_username"]',
            "password": '//*[@id="id_password"]',
            "login_button": '//*[@id="panel-login"]/div[2]/button',
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
        url = f"http://91hct.com:8054/xadmin/jiedai/userreg/"
        # 请求url
        response = session.get(url, headers=headers)
        # 获取结果
        html = Selector(text=response.text)
        result = {
            "注册人数": html.xpath('//*[@id="changelist-form"]/div/table/tbody/tr/td[3]/text()').re('(\d+)')[0],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": ""
        }
        self.write_sql(result)


SH = {
    "login_url": 'http://91hct.com:8054/xadmin/',
    "area": "",
    "product": "锦鲤钱包",
    "username": "g94",
    "password": "abc123456",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(600)














