# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 22:17
# @Author  : 逗比i
# @Project : Backstage
# @File    : 点容宝.py
# @Software: PyCharm
# @Describe:

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
            "username": '//*[@id="userAccount"]',
            "password": '//*[@id="userPassword"]',
            "login_button": '//*[@id="loginForm"]/div[4]/div/input',
            "check_code": '//*[@id="captcha"]',
            "code_image_url": '//*[@id="captchaBtn"]',
            "success_ele": '//*[@id="mCSB_1_container"]/ul[1]/li[1]/a[1]'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (300, 376, 600, 405), "30400")
        # 将cookie设置给session
        session.cookies.update(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        page_url = f"http://openback.hongzigame.com/channel/getChannelStatistics?channelName=&channelCode={self.channel}&startDate={self.today}&endDate=&numPerPage=10&pageNum=1&xzOldPageNum=1"
        # 请求url
        response = session.get(page_url, headers=headers)
        # 构造Selector
        selector = Selector(text=response.text)
        # 获取数据
        info = selector.xpath('//*[@id="bigDataList"]/tbody/tr/td/text()').extract()
        print(info)
        # 获取结果
        result = {
            "注册人数": info[4],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null"
        }
        self.write_sql(result)
        print(result)


SH = {
    "login_url": "http://openback.hongzigame.com/user/login",
    "area": "上海",
    "product": "小黄鱼",
    "username": "13816468838",
    "password": "123456",
    "channel": "Y163"
}

WD = {
    "login_url": "http://openback.hongzigame.com/user/login",
    "area": "外地",
    "product": "小黄鱼",
    "username": "15300920506",
    "password": "123456",
    "channel": "Y104"
}


all_area = [SH, WD]

while True:
    for each in all_area:
        XHY(each).get_info()
    sleep(1200)













