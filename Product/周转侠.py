#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/21 0021 9:45 
# @Author : Chihiro 
# @Site :  
# @File : 周转侠.py 
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
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        url = "http://yuehuixinxi.com/third_spreads/?token=fba3b33f205e6407880799168534c72ef3b7272b9ecc90f3e9dae088e6aa1286"
        # 请求url
        session = Session()
        response = session.get(url,headers=headers)
        # 构造Selector
        html = Selector(text=response.text)
        info = html.xpath('//*[@id="format_canal_register_feedback"]/text()').re('(\d+)')[0]

        # 获取数据
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


SH = {
    "login_url": "http://jincus.lsyaoji.cn/#/login",
    "area": "",
    "product": "金多宝",
    "username": "dkgj393",
    "password": "dkgj393",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        XHY(each).get_info()
        sleep(1200)
