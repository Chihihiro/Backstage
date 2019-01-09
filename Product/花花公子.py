#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/7 0007 16:50 
# @Author : Chihiro 
# @Site :  
# @File : 花花公子.py 
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
            "username": '//*[@id="main"]/div/div/div/div[2]/div/form/div[1]/div/div/input',
            "password": '//*[@id="main"]/div/div/div/div[2]/div/form/div[2]/div/div/input',
            "login_button": '//*[@id="main"]/div/div/div/div[2]/div/form/div[5]/div/button',
            "check_code": '//*[@id="main"]/div/div/div/div[2]/div/form/div[4]/div/div/input',
            "code_image_url": '//*[@id="s-canvas"]',
            "success_ele": '//*[@id="main"]/div/div[1]/div/div[3]/div/div/div/div/a/span'
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
        page_url = 'http://timedata.dgliao.cn/api/Bussiness/GetPartyBStatDataInfo?PartyBId=106'
        # 请求url
        response = session.get(page_url, headers=headers)
        # 构造Selector
        selector = response.json()
        # 获取数据
        print(selector)
        # info = selector.xpath('//*[@id="bigDataList"]/tbody/tr/td/text()').extract()
        # 获取结果
        # result = {
        #     "注册人数": info[2],
        #     "实名人数": info[3],
        #     "申请人数": "null",
        #     "放款人数": "null"
        # }
        # self.write_sql(result)



WD = {
    "login_url": "http://gzcus.michlhole.cn/#/login",
    "area": "外地",
    "product": "花花公子",
    "username": "hhgz105",
    "password": "hhgz105",
    "channel": ""
}


all_area = [WD]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(1200)