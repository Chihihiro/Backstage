#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/3 0003 17:06 
# @Author : Chihiro 
# @Site :  
# @File : 爱卡钱包.py 
# @Software: PyCharm



from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep
import time


class DRB(BaseSpider):

    def __init__(self, account):
        super(DRB, self).__init__(account)

    def get_info(self):
        # 设置session
        session = Session()
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
            "accessToken": "e8df476104c14452ef74f4eb3b275a57",
            "Origin": "http://akqb.zaixianjieshu.com",
            "Referer": "http://akqb.zaixianjieshu.com/H5/flowAdmin/index.html",
            "Content-Type": "application/json; charset=utf-8"
        }
        # 页面url
        json_url = "http://101.37.187.240:88/channel/admin/data"
        args = {
            'channelCode': "2019010114XMRBG",
            'merchantId': "0",
            'registerBeginDate': int(
                time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S"))) * 1000,
            'registerEndDate': int(
                time.mktime(time.strptime(f"{self.tomorrow} 00:00:00", "%Y-%m-%d %H:%M:%S"))) * 1000
        }
        # 请求url
        response = session.post(json_url, headers=headers, json=args)
        # info = response.json()
        # print(info)
        info = response.json()['data']['channelDataList'][0]
        # 获取结果
        print(info)
        result = {
            "注册人数": info['registerCount'],
            "实名人数": "null",
            "申请人数": info['applyCount'],
            "放款人数": info['agreeCount']
        }
        print(result)
        self.write_sql(result)




SH = {
    "login_url": "http://akqb.zaixianjieshu.com/H5/flowAdmin/index.html#/user/login",
    "area": "四平",
    "product": "爱卡钱包",
    "username": "aika1",
    "password": "123456",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        DRB(each).get_info()
        sleep(1200)



