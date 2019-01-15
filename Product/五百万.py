#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/14 0014 10:19 
# @Author : Chihiro 
# @Site :  
# @File : 五百万.py
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
            "username": '/html/body/div/form/input[1]',
            "password": '/html/body/div/form/input[2]',
            "login_button": '/html/body/div/form/input[4]',
            "check_code": '/html/body/div/form/input[3]',
            "code_image_url": '/html/body/div/form/img',
            "success_ele": '/html/body/div[1]/ul/li[2]/a'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (502, 390, 638, 439), "10400")
        # 将cookie设置给session
        session.cookies.update(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        page_url = "http://www.lovezcm.com/ymd/admin/channel-view.jsp?id=0.7025606997962637"
        # 请求url
        response = session.get(page_url, headers=headers)
        # 构造Selector
        html = Selector(text=response.text)
        # 获取结果
        result = {
            "注册人数": html.xpath('/html/body/div[1]/div[2]/table//tr[2]/td[3]/text()').extract()[0],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": ""
        }
        self.write_sql(result)
        print(result)


SH = {
    "login_url": "http://www.lovezcm.com/ymd/admin/htlogin.html",
    "area": "",
    "product": "五百万",
    "username": "sd",
    "password": "123",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        XHY(each).get_info()
        sleep(1200)

