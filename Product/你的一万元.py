#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/2 0002 11:07 
# @Author : Chihiro 
# @Site :  
# @File : 你的一万元.py 
# @Software: PyCharm



from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
import time
import warnings


class BJZ(BaseSpider):
    def __init__(self, account):
        super(BJZ, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="username"]',
            "password": '//*[@id="password"]',
            "login_button": '//*[@id="loginBtn"]',
            "check_code": "",
            "code_image_url": "",
            "success_ele": ""
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.no_check_get_cookie(xpath_info)
        # 给session设置cookie
        session.cookies.update(cookie_to_dict(cookie))
        # json的url
        url = 'http://channel.mgshujia.com/api?cmd=chluserTotal'
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        #postn内容
        arg = {'cnds': f'%7B%22date_FROM_cnd%22%3A%22{self.today}%22%2C%22date_TO_cnd%22%3A%22{self.today}%22%2C%22channel_path_cnd%22%3A%22%22%2C%22is_fuzzy_cnd%22%3A%22%22%7D'}
        # 访问url
        response = session.post(url, headers=headers, data=arg)
        # print(response.status_code)
        # print(response.json())
        json_info = response.json()["rows"]

        result = {
            "注册人数": json_info["register_num"],
            "实名人数": json_info['complete_info_num'],
            "申请人数": 'null',
            "放款人数": json_info['credit_pass_num']
        }
        self.write_sql(result)


SH = {
    "login_url": 'http://channel.mgshujia.com/',
    "area": "上海",
    "product": "你的一万元",
    "username": "ND2007",
    "password": "ND2007185",
    "channel": ""
}



all_local = [SH]



while True:
    for each in all_local:
        BJZ(each).get_info()
    time.sleep(1200)