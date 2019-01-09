#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/9 0009 15:12 
# @Author : Chihiro 
# @Site :  
# @File : 借你花.py 
# @Software: PyCharm


from selenium import webdriver
from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
import json
from time import sleep
import time

class BJZ(BaseSpider):
    def __init__(self, account):
        super(BJZ, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="itemBox"]/div[1]/input',
            "password": '//*[@id="itemBox"]/div[2]/input',
            "login_button": '//*[@id="main-content"]/div/div/form/div[2]/button',
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
        print(cookie_to_dict(cookie))
        # json的url
        url = f"http://qd.jienihua100.com/Admin/Ditchs/indexAjax.html?start={self.today}&end={self.today}&url={self.channel}&sEcho=3&iColumns=3&sColumns=%2C%2C&iDisplayStart=0&iDisplayLength=10&mDataProp_0=date_text&sSearch_0=&bRegex_0=false&bSearchable_0=true&mDataProp_1=gl_nreg&sSearch_1=&bRegex_1=false&bSearchable_1=true&mDataProp_2=gl_login&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch=&bRegex=false&_={str(int(time.time()*1000))}"#{str(int(time.time()*1000))}
        # url = f"http://qd.jienihua100.com/Admin/Ditchs/indexAjax.html?start=2019-01-09&end=2019-01-09&url=wyx03&sEcho=13&iColumns=3&sColumns=%2C%2C&iDisplayStart=0&iDisplayLength=10&mDataProp_0=date_text&sSearch_0=&bRegex_0=false&bSearchable_0=true&mDataProp_1=gl_nreg&sSearch_1=&bRegex_1=false&bSearchable_1=true&mDataProp_2=gl_login&sSearch_2=&bRegex_2=false&bSearchable_2=true&sSearch=&bRegex=false&_=1547018390672"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }


        # 访问url
        response = session.get(url, headers=headers)
        json_info = response.json()['data'][0]
        print(json_info)

        result = {
            "注册人数": json_info["gl_nreg"],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": ""
        }
        self.write_sql(result)


SH = {
    "login_url": "http://qd.jienihua100.com/Admin/Public/login.html",
    "area": "",
    "product": "借你花",
    "username": "WYX",
    "password": "WYX123",
    "channel": "wyx03"
}


all_local = [SH]
for each_local in all_local:
    spider = BJZ(each_local)
    spider.get_info()
