#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/4 0004 9:58 
# @Author : Chihiro 
# @Site :  
# @File : 大脸猫.py 
# @Software: PyCharm


from time import sleep
import requests
from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep


class DLM(BaseSpider):
    def __init__(self, account):
        super(DLM, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="name"]',
            "password": '//*[@id="login"]/div[2]/input',
            "login_button": '//*[@id="login"]/div[4]/div[2]/button',
            "check_code": '//*[@id="login"]/div[3]/input',
            "code_image_url": '//*[@id="captcha"]',
            "success_ele": '/html/body/div/div[1]/ul[2]/li[2]/a'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (453, 319, 579, 357), "30400")
        # 将cookie设置给session
        print(cookie)
        # 页面url
        page_url = f"https://channel.9281e.cn/index/index.shtml?start_time={self.today}&end_time={self.tomorrow}&channel=170"
        # 生成头部信息
        x = ''
        for i in range(len(cookie)):
            value = cookie[i]['name'] +'='+ cookie[i]['value'] + '; '
            x = x + value
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
            "cookie": "usermember=fx60; " + x
        }
        # session
        session = requests.session()
        response = session.get(page_url, headers=headers)

        # 构建selector
        selector = Selector(text=response.text)
        # 获取数据
        info = selector.xpath('/html/body/div/table[1]/tbody/tr/td/text()').extract()
        # 获取结果
        result = {
            "注册人数": info[0],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": info[1]
        }
        self.write_sql(result)


# 实例化对象
product = DLM({
    "login_url": "https://channel.9281e.cn/login/login.shtml",
    "area": "外地",
    "product": "大脸猫",
    "username": "fx60",
    "password": "123456",
    "channel": ""
})

while True:
    product.get_info()
    sleep(600)
















