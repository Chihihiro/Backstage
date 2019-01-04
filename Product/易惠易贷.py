#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/2 0002 18:05 
# @Author : Chihiro 
# @Site :  
# @File : 易惠易贷.py 
# @Software: PyCharm

import re
from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
import time
import warnings
from scrapy import Selector


class BJZ(BaseSpider):
    def __init__(self, account):
        super(BJZ, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="pd-form-username"]',
            "password": '//*[@id="pd-form-password"]',
            "login_button": '//*[@id="login-form"]/div[5]/button',
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
        # json的url
        url = f"https://www.gglcqm.cn/admin/channel/counts/ids/83?addtabs=1"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 访问url

        response = session.get(url, headers=headers)
        selector = Selector(text=response.text)
        apply = selector.xpath('//tbody/tr/td[3]/text()').extract()[0]
        print(apply)

        result = {
            "注册人数": re.sub('人', '', apply),
            "实名人数": "null",
            "申请人数": 'null',
            "放款人数": "null"
        }
        self.write_sql(result)


SH = {
    "login_url": 'https://www.gglcqm.cn/admin/index/login.html',
    "area": "外地",
    "product": "易惠易贷",
    "username": "18127438184",
    "password": "123456",
    "channel": ""
}


all_local = [SH]


while True:
    for each in all_local:
        BJZ(each).get_info()
    time.sleep(600)
