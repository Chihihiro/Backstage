#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/11 0011 16:39 
# @Author : Chihiro 
# @Site :  
# @File : 万赢宝.py 
# @Software: PyCharm




import time
from requests import Session
from scrapy import Selector
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict


class YQS(BaseSpider):
    def __init__(self, account):
        super(YQS, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="account"]',
            "password": '//*[@id="password"]',
            "login_button": '/html/body/div[2]/div/form/div[4]/button',
            "check_code": '//*[@id="checkCode"]',
            "code_image_url": '//*[@id="check_code"]',
            "success_ele": '//*[@id="topbar-collapse"]/ul/li[1]/a'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (345, 365, 439, 403), "10400")
        # 给session设置cookie
        session.cookies.update(cookie_to_dict(cookie))
        # page的url
        page_url = "https://tg.shhlwlkj.com/customer/list.htm"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        arg = {
            'mobile': "",
            'status': "",
            'brokerId': "",
            'gmtCreateStart': f"{self.today}",
            'gmtCreateEnd': f"{self.today}",
            'currentPage': 1
        }
        # 访问url
        response = session.post(page_url, headers=headers, data=arg)
        # 获取html
        info = Selector(text=response.text)
        print(response.text)
        # 最终结果

        result = {
            "注册人数": info.xpath('/html/body/div[1]/div[2]/div/div[3]/div/div/div/div/p/span/text()').extract()[0],
            "实名人数": "null",
            "申请人数": 'null',
            "放款人数": 'null',
            "备注": ""
        }
        self.write_sql(result)


SH = {
    "login_url": "https://tg.shhlwlkj.com/",
    "area": "",
    "product": "万赢宝",
    "username": "29640001",
    "password": "123456",
    "channel": ""
}


all_local = [SH]

while True:
    for each in all_local:
        YQS(each).get_info()
    time.sleep(1200)

