#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/9 0009 12:40 
# @Author : Chihiro 
# @Site :  
# @File : 好好贷.py 
# @Software: PyCharm



import re
from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
import time
import warnings
from scrapy import Selector
import json


class DLM(BaseSpider):
    def __init__(self, account):
        super(DLM, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="account"]',
            "password": '//*[@id="password"]',
            "login_button": '//*[@id="root"]/div/div/div[2]/div/form/div[4]/div/div/span/button',
            "check_code": '//*[@id="imgCode"]',
            "code_image_url": '//*[@id="root"]/div/div/div[2]/div/form/div[3]/div/div/span/div/div[2]/img',
            "success_ele": '//*[@id="root"]/div/div/div[1]/div/div/span/span'
        }
        # 获取cookie
        token = self.check_get_token(xpath_info, (565, 352, 653, 385), "30400", 'accessToken')

        # 页面url
        json_url = "http://47.110.6.255:2013/channel/admin/data"
        # 获取cookie
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
            'accessToken': token,
        }

        arg = {
            'channelCode': "2018122623XZPLJ",
            'merchantId': "0",
            'registerBeginDate': int(time.time() * 1000),
            'registerEndDate': int(time.time() * 1000)
        }
        session = Session()

        # 构建selector
        # 请求url
        response = session.post(json_url, headers=headers, json=arg)
        # 获取html
        info = response.json()['data']['channelDataList'][0]
        # print(info)
        result = {
            "注册人数": "null",
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": info['loanCount'],
            "备注": "放款产品"
        }
        self.write_sql(result)


SH = {
    "login_url": 'http://ahrzd.zaixianjieshu.com/ahrzd/H5/flowAdmin/index.html#/user/login',
    "area": "",
    "product": "好好贷",
    "username": "dapangzhi",
    "password": "123456",
    "channel": ""
}


all_local = [SH]


while True:
    for each in all_local:
        DLM(each).get_info()
    time.sleep(1200)