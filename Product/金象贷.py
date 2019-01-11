#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/11 0011 11:43 
# @Author : Chihiro 
# @Site :  
# @File : 金象贷.py 
# @Software: PyCharm


# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 21:56
# @Author  : 逗比i
# @Project : Backstage
# @File    : 抱金砖.py
# @Software: PyCharm
# @Describe:
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
            "username": '//*[@id="zhanghao"]',
            "password": '//*[@id="mima"]',
            "login_button": '/html/body/div/div/div/div[4]/a',
            "check_code": '//*[@id="verify"]',
            "code_image_url": '/html/body/div/div/div/div[3]/img',
            "success_ele": '/html/body/div[1]/ul/li[4]/a'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (432, 319, 542, 372), "10400")
        session.cookies.update(cookie_to_dict(cookie))
        # page的url
        page_url = f"https://vip.leyongqian.com/Mydata/?s_time={self.today}&e_time={self.today}"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }
        # 访问url
        response = session.get(page_url, headers=headers)
        # 获取html
        info = Selector(text=response.text)
        # 最终结果
        result = {
            "注册人数": info.xpath('//*[@id="tb_iu_app"]/tr/td[3]/text()').extract()[0],
            "实名人数": "null",
            "申请人数": 'null',
            "放款人数": 'null',
            "备注": ''
        }
        print(result)
        self.write_sql(result)


SH = {
    "login_url": "https://vip.leyongqian.com/",
    "area": "",
    "product": "金象贷",
    "username": "qianzhijia461",
    "password": "123456",
    "channel": "",

}

all_local = [SH]

while True:
    for each in all_local:
        YQS(each).get_info()
    time.sleep(1200)










