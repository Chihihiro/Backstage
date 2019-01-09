#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/7 0007 17:33 
# @Author : Chihiro 
# @Site :  
# @File : 朱八借.py 
# @Software: PyCharm



import json
from scrapy import Selector
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
            "username": '//*[@id="txtName"]',
            "password": '//*[@id="txtPwd"]',
            "login_button": '//*[@id="btnLogin"]',
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
        url = "https://zbjhhr.fen360.com/HHRLogin/HomePage?type=1"
        # 请求url
        response = session.get(url, headers=headers)
        # print(response.status_code)
        html = response.text
        info = Selector(text=html)
        # 获取结果
        result = {
            "注册人数": info.xpath('/html/body/div/div[3]/table//tr[1]/td[3]/a/text()').extract()[0],
            "实名人数": info.xpath('/html/body/div/div[3]/table//tr[1]/td[1]/a/text()').extract()[0],
            "申请人数": "null",
            "放款人数": info.xpath('/html/body/div/div[3]/table//tr[1]/td[2]/a/text()').extract()[0]
        }
        self.write_sql(result)


WD = {
    "login_url": 'https://zbjhhr.fen360.com/HHRLogin/Login/',
    "area": "上海",
    "product": "朱八借",
    "username": "13800000815",
    "password": "123456",
    "channel": ""
}


all_area = [WD]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(1200)
