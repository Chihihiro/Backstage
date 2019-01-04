#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/3 0003 11:14 
# @Author : Chihiro 
# @Site :  
# @File : 随心花.py 
# @Software: PyCharm



#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/3 0003 10:33
# @Author : Chihiro
# @Site :
# @File : 万达优卡.py
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
        xpath_info = {
            "username": '//*[@id="username"]',
            "password": '//*[@id="password"]',
            "login_button": '//*[@id="loginBtn"]',
            "check_code": '',
            "code_image_url": '',
            "success_ele": ''
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
        page_url = f"http://cnl.cangnanmingwei.com/api?cmd=chluserTotal"
        #参数
        arg = {
            'cnds': f'%7B%22date_FROM_cnd%22%3A%22{self.today}%22%2C%22date_TO_cnd%22%3A%22{self.today}%22%2C%22channel_path_cnd%22%3A%22%22%2C%22is_fuzzy_cnd%22%3A%22%22%7D'
        }
        # 请求url
        response = session.post(page_url, headers=headers, data=arg)
        # 构造Selector
        data = response.json()['rows']
        print(data)


        # 获取结果
        result = {
            "注册人数": data['register_num'],
            "实名人数": data["complete_info_num"],
            "申请人数": "null",
            "放款人数": data["credit_pass_money"]
        }
        self.write_sql(result)
        print(result)


WD = {
    "login_url": "http://cnl.cangnanmingwei.com/login",
    "area": "外地",
    "product": "随心花",
    "username": "qd2150",
    "password": "qd2150202",
    "channel": ""
}


all_area = [WD]


for each in all_area:
    XHY(each).get_info()
    sleep(1200)



