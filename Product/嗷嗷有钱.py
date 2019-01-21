#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/21 0021 9:51 
# @Author : Chihiro 
# @Site :  
# @File : 嗷嗷有钱.py 
# @Software: PyCharm



from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep



class XHY(BaseSpider):
    def __init__(self, account):
        super(XHY, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="username"]',
            "password": '//*[@id="password"]',
            "login_button": '//*[@id="btn_login"]',
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.no_check_get_cookie(xpath_info)
        # 将cookie设置给session
        session.cookies.update(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        url = f"http://www.chaorenqianbao.com/qc/indexdata/?page=1&limit=20&mobile=&time_reg={self.today}+-+{self.today}&time_active="
        # 请求url

        response = session.get(url, headers=headers)
        # 构造Selector
        info = response.json()
        # 获取结果
        result = {
            "注册人数": info['count'],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            '备注':''
        }
        self.write_sql(result)


SH = {
    "login_url": "http://www.chaorenqianbao.com/qc/login",
    "area": "",
    "product": "嗷嗷有钱",
    "username": "wolaiaayq",
    "password": "123456",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        XHY(each).get_info()
        sleep(1200)