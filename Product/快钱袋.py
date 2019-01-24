#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/22 0022 11:04 
# @Author : Chihiro 
# @Site :  
# @File : 快钱袋.py 
# @Software: PyCharm




from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep
import json


class XHY(BaseSpider):
    def __init__(self, account):
        super(XHY, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="login"]/form/div/input[1]',
            "password": '//*[@id="login"]/form/div/input[2]',
            "login_button": '//*[@id="login"]/form/button',
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
        url = "https://toupin.cn/qianbaoadm/channel/list"
        # 请求url
        arg = {
            'addtime_endtime': f"{self.today}",
            'addtime_starttime': f"{self.today}",
            'currentpage': "1"
        }
        response = session.post(url, headers=headers, json=json.dumps(arg))
        # 构造Selector
        info = response.json()['data']
        print(info)
        # 获取结果
        result = {
            "注册人数": info['listnum'],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            '备注':''
        }
        self.write_sql(result)


SH = {
    "login_url": "https://toupin.cn/web/channel/",
    "area": "",
    "product": "快钱袋",
    "username": "kqhzqz01",
    "password": "112233",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        XHY(each).get_info()
        sleep(600)