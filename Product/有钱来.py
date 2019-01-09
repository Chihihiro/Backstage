#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/7 0007 17:03 
# @Author : Chihiro 
# @Site :  
# @File : 有钱来.py 
# @Software: PyCharm


import json
from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep


class DRB(BaseSpider):
    def __init__(self, account):
        super(DRB, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="login"]/form/div/input[1]',
            "password": '//*[@id="login"]/form/div/input[2]',
            "login_button": '//*[@id="login"]/form/button',
            "check_code": '',
            "code_image_url": '',
            "success_ele": ''
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = cookie_to_dict(self.no_check_get_cookie(xpath_info))
        # cookie["pagenum"] = "200"
        # 将cookie设置给session
        session.cookies.update(cookie)
        # print(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        json_url = "https://toupin.cn/qianbaoadm/channel/list"
        # 请求url
        #post
        arg = {
            'addtime_endtime': f'{self.today}',
            'addtime_starttime': f'{self.tomorrow}',
            'currentpage': "1"
        }
        response = session.post(json_url, headers=headers, json=json.dumps(arg))
        # print(response.text)
        # print(response.status_code)
        info = response.json()['data']
        # 获取结果
        result = {
            "注册人数": info['listnum'],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null"
        }
        self.write_sql(result)


WD = {
    "login_url": 'https://toupin.cn/web/channel/',
    "area": "上海",
    "product": "有钱来",
    "username": "1788qkgj",
    "password": "123456",
    "channel": ""
}


all_area = [WD]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(1200)
