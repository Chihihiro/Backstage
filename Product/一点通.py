#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/2 0002 16:14 
# @Author : Chihiro 
# @Site :  
# @File : 一点通.py 
# @Software: PyCharm



from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep
import time
import json


class DRB(BaseSpider):
    def __init__(self, account):
        super(DRB, self).__init__(account)


    def get_info(self):
    #     # 设置session
        session = Session()
        # 设置头部信息
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "accessToken": "8e51020324b26b7e64469e5a11360b98",
            "Origin": "http://wxqz.zaixianjieshu.com",
            "Referer": "http://wxqz.zaixianjieshu.com/wxqz/H5/flowAdmin/index.html",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
            # "Access-Control-Allow-Headers": 'Content-Type,Accept,X-Requested-With,remember-me,bid,accessToken,productCategory,appCode'
         }
        # 页面url
        page_url = "http://47.110.6.255:2015/channel/admin/data"
        # post参数
        arg = {
            'channelCode': "2019010212BZYWG",
            'merchantId': "0",
            'registerBeginDate': int(time.time() * 1000),
            'registerEndDate': int(time.time() * 1000),
        }
        print(arg)
        # 请求url
        # 请求url
        response = session.post(page_url, headers=headers, json=arg)
        # 获取html
        info = response.json()['data']['channelDataList'][0]
        print(info)

        # 获取结果
        result = {
            "注册人数": info['registerCount'],
            "实名人数": "null",
            "申请人数": info["applyCount"],
            "放款人数": info['agreeCount']
        }
        self.write_sql(result)


SH = {
    "login_url": "http://wxqz.zaixianjieshu.com/wxqz/H5/flowAdmin/index.html#/user/login",
    "area": "上海",
    "product": "一点通",
    "username": "yun",
    "password": "123456",
    "channel": ""
}

all_area = [SH]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(1200)
