# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 21:56
# @Author  : 逗比i
# @Project : Backstage
# @File    : 鑫融钱庄.py
# @Software: PyCharm
# @Describe:

from scrapy import Selector
from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
import time


class BJZ(BaseSpider):
    def __init__(self, account):
        super(BJZ, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="loginForm"]/div[1]/div/input',
            "password": '//*[@id="loginForm"]/div[2]/div/input',
            "login_button": '//*[@id="loginForm"]/button',
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
        page_url = 'http://kysmart.com.cn/Xrqz/action/basicExtensionLink/see?model.oid=I820VHGQ91'
        # 请求url
        response = session.get(page_url, headers=headers)
        # 获取html
        html = response.text
        # 构造选择器
        selector = Selector(text=html)
        info = selector.xpath('//*[@id="tab1"]/table//tr[2]/td[2]/text()').extract()
        # 获取结果
        result = {
            "注册人数": info[0],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null"
        }
        self.write_sql(result)


SH = {
    "login_url": "http://kysmart.com.cn/Xrqz/action/manageAdmin/doLogout",
    "area": "上海",
    "product": "鑫融钱庄",
    "username": "qudaoA15",
    "password": "123456",
    "channel": ""
}


all_local = [SH]

while True:
    for each in all_local:
        BJZ(each).get_info()
    time.sleep(600)



