#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/3 0003 11:38 
# @Author : Chihiro 
# @Site :  
# @File : 豪顺借.py 
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
            "username": '//*[@id="username"]',
            "password": '//*[@id="password"]',
            "login_button": '//*[@id="logina"]',
            "check_code": '',
            "code_image_url": '',
            "success_ele": ''
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
        page_url = "http://haoshun.youdaikeji.com/mgmt/thirdChannel/channelStatistics?channelId=94"
        #参数
        arg = {
            'startDateTime': f'{self.today}',
            # 'channelId':,
            'page': 1,
            'rows': 10,
        }
        # 请求url
        response = session.post(page_url, headers=headers, data=arg)
        # 构造Selector
        data = response.json()['rows'][0]
        print(data)


        # 获取结果
        result = {
            "注册人数": data['countUser'],
            "实名人数": 'null',
            "申请人数": data['countApply'],
            "放款人数": "null"
        }
        self.write_sql(result)
        print(result)


WD = {
    "login_url": "http://haoshun.youdaikeji.com/mgmt/login",
    "area": "外地",
    "product": "豪顺借",
    "username": "cai8",
    "password": "123456",
    "channel": ""
}


all_area = [WD]


for each in all_area:
    XHY(each).get_info()
    sleep(1200)
