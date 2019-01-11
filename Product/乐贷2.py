#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/10 0010 16:24 
# @Author : Chihiro 
# @Site :  
# @File : 乐贷2.py 
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
            "password": '//*[@id="password"]',
            "login_button": '/html/body/div/div/div/form/div[4]',
            "check_code": '//*[@id="captcha"]',
            "code_image_url": '//*[@id="validateCodeImg"]',
            "success_ele": '/html/body/div/div[1]/div[2]/ul'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (507, 487, 638, 530), "10400")
        # 给session设置cookie
        session.cookies.update(cookie_to_dict(cookie))
        # page的url
        page_url = "http://partner.ytrong.com/partner/info?id=310&page=1&limit=30"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        arg = {
            'id': 310,
            'page': 1,
            'limit': 30
        }
        # 访问url
        response = session.post(page_url, headers=headers, data=arg)
        # 获取html
        info = response.json()['rows'][0]
        # print(info)
        # 最终结果

        result = {
            "注册人数": info['userCount'],
            "实名人数": "null",
            "申请人数": 'null',
            "放款人数": 'null',
            "备注": ""
        }
        self.write_sql(result)


SH = {
    "login_url": "http://partner.ytrong.com/partner/login",
    "area": "",
    "product": "乐贷2",
    "username": "klsq",
    "password": "456123",
    "channel": ""
}


all_local = [SH]

while True:
    for each in all_local:
        YQS(each).get_info()
    time.sleep(1200)
