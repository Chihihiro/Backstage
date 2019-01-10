#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/10 0010 11:18 
# @Author : Chihiro 
# @Site :  
# @File : 简信宝.py 
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

        # 设置session
        session = Session()
        # 设置头部信息
        headers = {
            "Cookie": "PHPSESSID=5952acdfd13035322e25ee7deadc25d8; XSRF-TOKEN=eyJpdiI6ImtXdjJiVnNNeWhTeWdSVUZaR21XTFE9PSIsInZhbHVlIjoibXJwazlnaFpsTFF6cXJYdEZcL25HZTdJR3ZOQ3cwNVdlMExPRGRUeml2TEZwM0ZmdmFcL0x3N1BRb3l2TmtzRkFUR1Z5Smd5aFFxdDhUeHU1ZkVzVjdlUT09IiwibWFjIjoiNjlkYjQyNzA5YTM5MTk2NmNjOTU4YTA3ZGQyMjYyMjUxOTAyOWFkMTI5ZGVkMTk5MWY0Njg1NmM4M2MxMzU5YSJ9; laravel_session=eyJpdiI6IkJpNCtNekV1VlBmXC9BV2MxeUxXbXRnPT0iLCJ2YWx1ZSI6IkxaV203RGRxN3FHUHdBWWZSTmwzelFBYWR0NWFycTc0N05cL09PejN5dUZJVHhURTJVT2M4R3owbXhsVWZwRXh6TVdVbURxMVBvbVFiMUZOY1V3V3d3Zz09IiwibWFjIjoiOWM5MTk4YzIwYWM4NzRmNzQxZjY2YmM2ZWMwNmQ5NzYwYjY4YjE3MmZkYzQ4OWIwY2FlYTE5ZmYwYjA0MWU5YyJ9",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        url = 'http://www.daohuixinxi.com/admin/promoter/user'
        #参数

        # 请求url
        response = session.get(url, headers=headers)
        # 构造Selector
        info = Selector(text=response.text)
        print(response.text)
        num = info.xpath('/html/body/div/div[1]/div[1]/div/font[2]/text()').extract()[0]
        print(num)
        # # 获取结果
        # result = {
        #     "注册人数": data['register_num'],
        #     "实名人数": data["complete_info_num"],
        #     "申请人数": "null",
        #     "放款人数": data["credit_pass_money"]
        # }
        # self.write_sql(result)
        # print(result)


WD = {
    "login_url": "",
    "area": "",
    "product": "",
    "username": "",
    "password": "",
    "channel": ""
}


all_area = [WD]


for each in all_area:
    XHY(each).get_info()
    sleep(1200)



