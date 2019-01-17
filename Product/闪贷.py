#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/10 0010 11:18 
# @Author : Chihiro 
# @Site :  
# @File : shandai.py
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

        # 设置session
        session = Session()
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        url = f'http://www.youxinsign.com:13083/youka/ope-channel/getChannelRegist?startDate={self.today}&endDate={self.today}&encCode=0A18A358F7C7B59C'
        #参数

        # 请求url
        response = session.get(url, headers=headers)
        # 构造Selector
        info = response.json()['data']["datas"][0]["outRegistCount"]
        print(info)
        # 获取结果
        result = {
            "注册人数": info,
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": ''
        }
        self.write_sql(result)
        print(result)


WD = {
    "login_url": "",
    "area": "",
    "product": "闪贷",
    "username": "",
    "password": "",
    "channel": ""
}


all_area = [WD]


for each in all_area:
    XHY(each).get_info()
    sleep(1200)




