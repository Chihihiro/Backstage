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
            "username": '//*[@id="rrapp"]/div[2]/div[1]/input',
            "password": '//*[@id="rrapp"]/div[2]/div[2]/input',
            "login_button": '//*[@id="rrapp"]/div[2]/div[4]/div[2]/button',
            "check_code": '//*[@id="rrapp"]/div[2]/div[3]/input',
            "code_image_url": '//*[@id="rrapp"]/div[2]/div[3]/img',
            "success_ele": '//*[@id="rrapp"]/header/nav/div[1]'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (525, 305, 633, 340), "30500")
        # 将cookie设置给session
        session.cookies.update(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        page_url = f"http://106.14.158.253:8090//getRegisterCount?_search=false&nd={str(int(time.time()*1000))}&size=10&current=1&sidx=&order=asc&startTime={self.today}&endTime={self.today}&channelCode=ka10&_={str(int(time.time()*1000))}"
        # 请求url
        response = session.get(page_url, headers=headers)
        # 构造Selector
        data = response.json()['records'][0]
        print(data)


        # 获取结果
        result = {
            "注册人数": data['registerCount'],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null"
        }
        self.write_sql(result)
        print(result)


SH = {
    "login_url": "http://106.14.158.253:8090/login.html",
    "area": "上海",
    "product": "万达优卡",
    "username": "ka10",
    "password": "a234234",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        XHY(each).get_info()
        sleep(1200)



