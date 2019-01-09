#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/9 0009 10:14 
# @Author : Chihiro 
# @Site :  
# @File : 一点通2.py 
# @Software: PyCharm




from time import sleep
import requests
from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep
import time

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
        json_url = "http://47.110.6.255:2015/channel/admin/data"
        # 获取cookie
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
            'Host': 'merchant.xianjinxia.com',
            'accessToken': token,
            'Origin': 'http: // wxqz.zaixianjieshu.com',
            'Referer': 'http: // wxqz.zaixianjieshu.com / wxqz / H5 / flowAdmin / index.html'

        }

        arg = {
            'channelCode': "2019010512OJHVP",
            'merchantId': "0",
            'registerBeginDate': int(time.time() * 1000),
            'registerEndDate': int(time.time() * 1000),
        }
        session = Session()

        # 构建selector
        # 请求url
        response = session.post(json_url, headers=headers, json=arg)
        # 获取html
        info = response.json()['data']['channelDataList'][0]
        print(info)

        # 获取结果
        result = {
            "注册人数": info['registerCount'],
            "实名人数": "null",
            "申请人数": info["applyCount"],
            "放款人数": info['agreeCount'],
            "备注": ""
        }
        self.write_sql(result)



SH = {
    "login_url": "http://wxqz.zaixianjieshu.com/wxqz/H5/flowAdmin/index.html#/user/login",
    "area": "上海",
    "product": "一点通",
    "username": "yy5",
    "password": "yy5",
    "channel": ""
}

all_area = [SH]

while True:
    for each in all_area:
        DLM(each).get_info()
    sleep(1200)
