#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/12/31 0031 11:22 
# @Author : Chihiro 
# @Site :  
# @File : 闪借宝.py 
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
            "username": '//*[@id="verifyPhone"]',
            "password": '//*[@id="verifyCode"]',
            "login_button": '/html/body/div[3]/div[1]/form/div[3]/button',
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
        print(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        page_url = "http://ppass.com.cn/action/adminPlatformQuery/getUserList"
        # 请求url
        #post
        arg = {
            'startTime': f'{self.today}',
            'endTime': f'{self.tomorrow}',
            'page': 0
        }
        response = session.post(page_url, headers=headers, data=arg)
        info = response.json()['countMassage']
        # 获取结果
        result = {
            "注册人数": info['registered'],
            "实名人数": "null",
            "申请人数": info['applied'],
            "放款人数": info['loans']
        }
        self.write_sql(result)




SH = {
    "login_url": "http://ppass.com.cn/pageList/platform/login.jsp",
    "area": "上海",
    "product": "闪借宝",
    "username": "13300000013",
    "password": "123456",
    "channel": ""
}

all_area = [SH]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(1200)