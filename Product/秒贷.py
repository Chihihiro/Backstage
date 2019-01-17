#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/16 0016 13:11 
# @Author : Chihiro 
# @Site :  
# @File : 秒贷.py
# @Software: PyCharm



from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep


class XHY(BaseSpider):
    def __init__(self, account):
        super(XHY, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="login-page-full"]/div/div[3]/form/ul/li[1]/input',
            "password": '//*[@id="login-page-full"]/div/div[3]/form/ul/li[2]/input',
            "login_button": '//*[@id="login-page-full"]/div/div[3]/form/ul/li[4]/button',
            "check_code": '//*[@id="login-page-full"]/div/div[3]/form/ul/li[3]/input',
            "code_image_url": '//*[@id="login-page-full"]/div/div[3]/form/ul/li[3]/span/img',
            "success_ele": '//*[@id="header-navbar"]/div/div[1]/ul/li/a/img'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (616, 405, 710, 438), "20300")
        # 将cookie设置给session
        session.cookies.update(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        page_url = f"http://0v10.cn/admin/customer/promote.html?start_time={self.today.year}%2F{str(100+int(self.today.month))[1:]}%2F{str(100+self.today.day)[1:]}+-+{self.tomorrow.year}%2F{str(100+int(self.tomorrow.month))[1:]}%2F{str(100+self.tomorrow.day)[1:]}"

        print(page_url)
        # 请求url
        response = session.get(page_url, headers=headers)
        # 构造Selector
        selector = Selector(text=response.text)
        # 获取数据
        info = selector.xpath('//*[@id="content-wrapper"]/div/div/div[2]/div/div/div/div[2]/form/table//tr/td[4]/text()').extract()[0]
        print(info)
        # 获取结果
        result = {
            "注册人数": info,
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            '备注':''
        }
        self.write_sql(result)
        print(result)


SH = {
    "login_url": "http://0v10.cn/admin/login.html",
    "area": "",
    "product": "秒贷",
    "username": "嘉乐金融2",
    "password": "123456",
    "channel": ""
}


all_area = [SH]


for each in all_area:
    XHY(each).get_info()
    sleep(1200)




