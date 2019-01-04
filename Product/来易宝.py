# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 21:56
# @Author  : 逗比i
# @Project : Backstage
# @File    : 抱金砖.py
# @Software: PyCharm
# @Describe:

import requests
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
import time


class BJZ(BaseSpider):
    def __init__(self, account):
        super(BJZ, self).__init__(account)

    def get_info(self):
        url = 'https://lyb.ruyibao88.com/lybmanage/tongji/user/cpa_tj'
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        args = {
            'channel': '5bf9588f3b0443089fc4e4b1fdbc8b86',
            'start_time': f'{self.today}',
            'end_time': f'{self.today}'
        }
        response = requests.post(url, headers=header, data=args)
        info = response.json()['data'][0]
        # 获取结果
        result = {
            "注册人数": info['reg'],
            "实名人数": info['sm'],
            "申请人数": info['apply'],
            "放款人数": info["apply1"]
        }
        self.write_sql(result)

WD = {
    "login_url": "",
    "area": "外地",
    "product": "来易宝",
    "username": "",
    "password": "",
    "channel": ""
}


all_local = [WD]

while True:
    for each in all_local:
        BJZ(each).get_info()
    time.sleep(600)



