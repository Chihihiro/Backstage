# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 22:17
# @Author  : 逗比i
# @Project : Backstage
# @File    : 点容宝.py
# @Software: PyCharm
# @Describe:

from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep
import json
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
            'Host': 'merchant.xianjinxia.com',
            'loginToken': '28307fbeda88ea82e7401562460a72668f607836e344de926321f3abfd0b7e082484894eb379064fbb6fad2ff81c2ee394ad8f165fbf7a460123e97d6ae1e360',
            'Origin': 'http://merchant.xianjinxia.com',
            'Referer': 'http://merchant.xianjinxia.com/'
        }
        # 页面url
        json_url = "http://merchant.xianjinxia.com/api/v2/merchant/admin/youmi/statisticsThirdPage"
        args = {
            'dtEnd': int(time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S")))*1000,
            'dtStart': int(time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S")))*1000,
            'dtRange': [int(time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S")))*1000,
                        int(time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S")))*1000],
            'channelName': self.channel
        }
        # 请求url
        response = session.post(json_url, headers=headers, json=args)
        # info = response.json()

        info = response.json()['data']['list'][0]
        # 获取结果
        result = {
            "注册人数": info['regCount'],
            "实名人数": "null",
            "申请人数": 'null',
            "放款人数": 'null'
        }
        print(result)
        self.write_sql(result)


WD = {
    "login_url": '',
    "area": "外地",
    "product": "有米管家",
    "username": "",
    "password": "",
    "channel": "ymgj-yfwk1"
}

SP = {
    "login_url": '',
    "area": "四平",
    "product": "有米管家",
    "username": "",
    "password": "",
    "channel": "有米管家-悦富万卡"
}


WD2 = {
    "login_url": '',
    "area": "外地",
    "product": "有米管家",
    "username": "",
    "password": "",
    "channel": "有米管家-悦富万卡"
}




all_area = [WD, SP]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(1200)













