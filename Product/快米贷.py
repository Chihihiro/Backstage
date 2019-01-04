#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/12/28 0028 16:26 
# @Author : Chihiro 
# @Site :  
# @File : 快米贷.py 
# @Software: PyCharm


import requests
from BaseSpider import BaseSpider
import time
import json

class BJZ(BaseSpider):
    def __init__(self, account):
        super(BJZ, self).__init__(account)

    def get_info(self):
        url = 'https://dapi.saaspd.com/v1/data/channelmanagement/list'
        header = {
            'Origin': 'https://admin.kuaimidai.com',
            'Referer': 'https://admin.kuaimidai.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        args = {
            'BalanceType': "",
            'BalanceWay': "",
            'DesId': "1c21c/wqOFk=",
            'EndTime': f"{self.today} 23:59:59",
            'Page': 1,
            'PageSize': 15,
            'SourceName': f"{self.channel}",
            'StartTime': f"{self.today} 00:00:00",
            'merchant': "kmd"
        }
        response = requests.post(url, headers=header, data=json.dumps(args))

        info = response.json()['Result']
        # 获取结果
        result = {
            "注册人数": info['TotalNumRegister'],
            "实名人数": info['TotalNumCert'],
            "申请人数": 'null',
            "放款人数": 'null'
        }
        self.write_sql(result)

SH = {
    "login_url": "",
    "area": "上海",
    "product": "快米贷",
    "username": "",
    "password": "",
    "channel": "laotie03"
}


all_local = [SH]

while True:
    for each in all_local:
        BJZ(each).get_info()
    time.sleep(600)