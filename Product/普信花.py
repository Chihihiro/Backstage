#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/14 0014 10:19 
# @Author : Chihiro 
# @Site :  
# @File : 普信花.py 
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
            "username": '//*[@id="itemBox"]/div[1]/input',
            "password": '//*[@id="itemBox"]/div[2]/input',
            "login_button": '//*[@id="main-content"]/div/div/form/div[2]/button/span[2]',
            "check_code": '//*[@id="itemBox"]/div[3]/input',
            "code_image_url": '//*[@id="itemBox"]/div[4]/img',
            "success_ele": '/html/body/div[1]/div/a'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (336, 373, 627, 458), "30500")
        # 将cookie设置给session
        session.cookies.update(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        page_url = f"http://pxhadmin.wx273.com/Business/Promote/my_data?start={self.today}&end={self.today}&youxiao="
        # 请求url
        response = session.get(page_url, headers=headers)
        # 构造Selector
        html = Selector(text=response.text)
        # 获取结果
        result = {
            "注册人数": html.xpath('//*[@id="main"]/div[4]/div/span[2]/text()').re('共\s*(\d+)\s*条记录')[0],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null"
        }
        self.write_sql(result)
        print(result)


SH = {
    "login_url": "http://pxhadmin.wx273.com/Business/Public/login.html",
    "area": "",
    "product": "普信花",
    "username": "速贷-苏",
    "password": "123456",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        XHY(each).get_info()
        sleep(1200)

