#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/10 0010 14:12 
# @Author : Chihiro 
# @Site :  
# @File : 全能贷.py 
# @Software: PyCharm



import time
from requests import Session
from scrapy import Selector
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict


class YQS(BaseSpider):
    def __init__(self, account):
        super(YQS, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="account"]',
            "password": '//*[@id="pwd"]',
            "login_button": '//*[@id="loginForm"]/div[5]/button',
            "check_code": '//*[@id="verify"]',
            "code_image_url": '//*[@id="verifyImg"]',
            "success_ele": '//*[@id="navbar-header"]/ul[1]/li[3]/a'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (563, 486, 656, 522), "30400")
        # 给session设置cookie
        session.cookies.update(cookie_to_dict(cookie))
        # page的url
        page_url = "https://quan.jsd0086.com/agent/report/index"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }

        # 访问url
        response = session.get(page_url, headers=headers)
        # 获取html
        info = Selector(text=response.text)
        print(response.text)
        # 最终结果

        result = {
            "注册人数": info.xpath('//table//tr/td[2]/text()').extract()[0],
            "实名人数": info.xpath('//table//tr/td[5]/text()').extract()[0],
            "申请人数": 'null',
            "放款人数": 'null',
            "备注": ""
        }
        self.write_sql(result)


SH = {
    "login_url": "https://quan.jsd0086.com/agent/home/login",
    "area": "",
    "product": "全能贷",
    "username": "quan1",
    "password": "123456",
    "channel": ""
}


all_local = [SH]

while True:
    for each in all_local:
        YQS(each).get_info()
    time.sleep(1200)
