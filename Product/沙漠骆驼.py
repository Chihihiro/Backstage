#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/12/29 0029 11:54 
# @Author : Chihiro 
# @Site :  
# @File : 沙漠骆驼.py 
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
            "username": '//*[@id="name"]',
            "password": '//*[@id="login"]/div[2]/input',
            "login_button": '//*[@id="login"]/div[4]/div[2]/button',
            "check_code": '//*[@id="login"]/div[3]/input',
            "code_image_url": '//*[@id="captcha"]',
            "success_ele": '/html/body/div/div[1]/ul[2]/li[1]'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (455, 315, 578, 355), "30400")
        # 将cookie设置给session
        session.cookies.update(cookie_to_dict(cookie))
        print(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        page_url = f"https://www.souwl.cn/admin/register/index.shtml?start_time={self.today}+00%3A00%3A00&end_time={self.tomorrow}+00%3A00%3A00&channel=337"
        # 请求url
        response = session.get(page_url, headers=headers)
        # 构造Selector
        selector = Selector(text=response.text)
        # 获取数据
        info = selector.xpath('/html/body/table[1]/tbody/tr/td/text()').extract()

        # 获取结果
        result = {
            "注册人数": info[0],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": info[1]
        }
        self.write_sql(result)


SH = {
    "login_url": "https://www.souwl.cn/admin/common/login.shtml",
    "area": "四平",
    "product": "沙漠骆驼",
    "username": "luotuo1",
    "password": "123456",
    "channel": ""
}

all_area = [SH]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(1200)