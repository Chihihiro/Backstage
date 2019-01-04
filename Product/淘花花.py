#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/12/28 0028 12:59 
# @Author : Chihiro 
# @Site :  
# @File : 淘花花.py 
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
            "username": '//*[@id="userAccount"]',
            "password": '//*[@id="userPassword"]',
            "login_button": '//*[@id="loginForm"]/div[4]/div/input',
            "check_code": '//*[@id="captcha"]',
            "code_image_url": '//*[@id="captchaBtn"]',
            "success_ele": '//*[@id="menu"]/li/ul/li/a/span[2]'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (300, 376, 600, 405), "30400")
        # 将cookie设置给session
        session.cookies.update(cookie_to_dict(cookie))
        print(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        page_url = f"http://open-admin.zhongguoqiumi.com/channel/getChannelStatistics?channelName=&channelCode=mimkd3&startDate=2018-12-28&endDate=2018-12-28&numPerPage=10&pageNum=1&xzOldPageNum=1"
        # 请求url
        response = session.get(page_url, headers=headers)
        # 构造Selector
        selector = Selector(text=response.text)
        # 获取数据
        info = selector.xpath('//*[@id="bigDataList"]/tbody/tr/td/text()').extract()
        # print(info)

        # 获取结果
        result = {
            "注册人数": info[4],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null"
        }
        self.write_sql(result)


SH = {
    "login_url": "http://open-admin.zhongguoqiumi.com/user/login",
    "area": "外地",
    "product": "淘花花",
    "username": "15927262353",
    "password": "123456",
    "channel": "mimkd3"
}

all_area = [SH]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(1200)
