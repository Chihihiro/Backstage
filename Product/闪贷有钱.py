#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/23 0023 16:05 
# @Author : Chihiro 
# @Site :  
# @File : 闪贷有钱.py 
# @Software: PyCharm






import requests
from scrapy import Selector
from BaseSpider import BaseSpider
from time import sleep


class CXBK(BaseSpider):
    def __init__(self, account):
        super(CXBK, self).__init__(account)

    def get_info(self):

        json_url = "http://www.youxinsign.com:13083/youka/ope-channel/getChannelRegist?encCode=B79E166DC41981EA"
        # 设置session
        session = requests.session()
        # 设置头部
        headers = {
            'Host': 'www.youxinsign.com:13083',
            'Origin': 'http://www.youxinsign.com',
            "Referer": "http://www.youxinsign.com/shandai_admin/channelMerchants.html?encCode=B79E166DC41981EA",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 访问url
        response = session.get(json_url, headers=headers)
        # 构建Selector
        info = response.json()['data']['datas'][0]
        print(info)
        # 获取认证用户

        result = {
            "注册人数": info['outRegistCount'],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": ''
        }
        self.write_sql(result)


WD = {
    "login_url": "",
    "area": "",
    "product": "闪贷有钱",
    "username": "",
    "password": "",
    "channel": ""
}

all_local = [WD]

while True:
    for each_local in all_local:
        spider = CXBK(each_local)
        spider.get_info()
    sleep(600)













