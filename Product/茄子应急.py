#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/21 0021 13:32 
# @Author : Chihiro 
# @Site :  
# @File : 茄子应急.py 
# @Software: PyCharm



from requests import Session
from BaseSpider import BaseSpider
from time import sleep
import time


class DRB(BaseSpider):
    def __init__(self, account):
        super(DRB, self).__init__(account)

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
        # 设置session
        session = Session()
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
            "accessToken": token,
            "Origin": "http://akqb.zaixianjieshu.com",
            "Referer": "http://akqb.zaixianjieshu.com/H5/flowAdmin/index.html",
            "Content-Type": "application/json; charset=utf-8"
        }
        # 页面url
        json_url = "http://101.37.191.5:2017/channel/admin/data"
        args = {
            'channelCode': self.channel,
            'merchantId': "0",
            'registerBeginDate': int(
                time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S"))) * 1000,
            'registerEndDate': int(
                time.mktime(time.strptime(f"{self.tomorrow} 00:00:00", "%Y-%m-%d %H:%M:%S"))) * 1000
        }
        # 请求url
        response = session.post(json_url, headers=headers, json=args)
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



WD = {
    "login_url": "http://fjnazx.zaixianjieshu.com/fjnazx/H5/flowAdmin/index.html#/user/login",
    "area": "",
    "product": "茄子应急",
    "username": "huang",
    "password": "123456",
    "channel": "2019011823AOQLS"
}


all_area = [WD]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(1200)