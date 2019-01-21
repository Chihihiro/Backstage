#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/10 0010 13:28 
# @Author : Chihiro 
# @Site :  
# @File : 超人钱包.py
# @Software: PyCharm



from BaseSpider import BaseSpider
from time import sleep
from requests import Session
from DealWithCookie import cookie_to_dict


class XHY(BaseSpider):
    def __init__(self, account):
        super(XHY, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="username"]',
            "password": '//*[@id="password"]',
            "login_button": '//*[@id="btn_login"]'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.no_check_get_cookie(xpath_info)
        # json的url
        json_url = f"http://www.chaorenqianbao.com/qc/indexdata/?page=1&limit=20&mobile=&time_reg={self.today}+-+{self.today}&time_active="
        # 设置session
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        session.cookies.update(cookie_to_dict(cookie))
        response = session.get(json_url, headers=headers)
        # 构造Selector
        info = response.json()
        print(info)


        # 获取结果
        result = {
            "注册人数": info['count'],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": ''
        }
        self.write_sql(result)


WD = {
    "login_url": "http://www.chaorenqianbao.com/qc/login",
    "area": "",
    "product": "超人钱包",
    "username": "xiaozhuqianbao",
    "password": "123456",
    "channel": ""
}

all_local = [WD]

while True:
    for each_local in all_local:
        spider = XHY(each_local)
        spider.get_info()
    sleep(600)













