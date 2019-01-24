#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/10 0010 13:28 
# @Author : Chihiro 
# @Site :  
# @File : 借小宝.py
# @Software: PyCharm




import requests
from scrapy import Selector
from BaseSpider import BaseSpider
from time import sleep


class CXBK(BaseSpider):
    def __init__(self, account):
        super(CXBK, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="loginform"]/form/div[1]/div/input',
            "password": '//*[@id="loginform"]/form/div[2]/div/input',
            "login_button": '//*[@id="login"]'
        }
        # 获取cookie
        cookie = self.no_check_get_cookie(xpath_info)
        # json的url
        json_url = f"http://jiexiaobao.9lwealth.com/Soleaoc/Platlogin/index"
        # 设置session
        session = requests.session()
        # 设置头部
        headers = {
            "Host": f"{cookie[0]['domain']}",
            "Referer": f"http://{cookie[0]['domain']}/Mwsad/Platlogin/index",
            "Origin": f"http://{cookie[0]['domain']}",
            "Cookie": f"{cookie[0]['name']}={cookie[0]['value']}; {cookie[1]['name']}={cookie[1]['value']}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 设置参数
        args = {
            "star_time": str(self.today),
            "end_time": str(self.today)
        }
        # 访问url
        response = session.post(json_url, headers=headers, data=args)
        # 构建Selector
        selector = Selector(text=response.text)
        # 获取认证用户
        apply_user = selector.xpath('/html/body/div/div[2]/div/span/strong[1]/text()').extract()[0]
        # 获取注册数量
        register_user = selector.xpath('/html/body/div/div[2]/div/span/strong[5]/text()').extract()[0]
        real_name = selector.xpath('/html/body/div/div[2]/div/span/strong[3]/text()').extract()[0]
        # 获取结果
        result = {
            "注册人数": apply_user,
            "实名人数": real_name,
            "申请人数": "null",
            "放款人数": register_user,
            "备注": ''
        }
        self.write_sql(result)


WD = {
    "login_url": "http://jiexiaobao.9lwealth.com/Soleaoc/Platlogin/index",
    "area": "",
    "product": "借小宝",
    "username": "ql28",
    "password": "123456",
    "channel": ""
}

all_local = [WD]

while True:
    for each_local in all_local:
        spider = CXBK(each_local)
        spider.get_info()
    sleep(600)













