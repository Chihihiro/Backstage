#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/7 0007 16:50 
# @Author : Chihiro 
# @Site :  
# @File : 花花公子.py 
# @Software: PyCharm




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
            "username": '//*[@id="main"]/div/div/div/div[2]/div/form/div[1]/div/div/input',
            "password": '//*[@id="main"]/div/div/div/div[2]/div/form/div[2]/div/div/input',
            "login_button": '//*[@id="main"]/div/div/div/div[2]/div/form/div[5]/div/button',
            "check_code": '//*[@id="main"]/div/div/div/div[2]/div/form/div[4]/div/div/input',
            "code_image_url": '//*[@id="s-canvas"]',
            "success_ele": '//*[@id="main"]/div/div[1]/div/div[3]/div/div/div/div/a/span'
        }
        # 获取html
        html = self.check_get_html(xpath_info, (369, 438, 516, 480), "10400")
        # 构造Selector
        selector = Selector(text=html)
        # 获取数据
        info = selector.xpath('/text()').re("(\d*)")
        # 获取结果
        result = {
            "注册人数": info[0],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null"
        }
        self.write_sql(result)



WD = {
    "login_url": "http://gzcus.michlhole.cn/#/login",
    "area": "外地",
    "product": "花花公子",
    "username": "hhgz171",
    "password": "hhgz171",
    "channel": ""
}


all_area = [WD]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(1200)