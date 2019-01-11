#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/11 0011 14:27 
# @Author : Chihiro 
# @Site :  
# @File : 萌新记账.py 
# @Software: PyCharm





import time
from requests import Session
from scrapy import Selector
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict


class YQS(BaseSpider):
    def __init__(self, account):
        super(YQS, self).__init__(account)
        self.chennel_id = account["id"]

    def get_info(self):
        # xpath_info = {
        #     "username": '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[1]/form/div[1]/div/div/input',
        #     "password": '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[1]/form/div[2]/div/div[1]/input',
        #     "login_button": '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[1]/div',
        #     "check_code": '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[1]/form/div[3]/div/div/input',
        #     "code_image_url": '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[1]/form/div[3]/div/img',
        #     "success_ele": '//*[@id="app"]/div/div[1]/div[3]/div/ul/li[1]/div'
        # }
        # 设置session
        session = Session()
        # 获取cookie
        # cookie = self.check_get_cookie(xpath_info, (535, 378, 615, 408), "30400")
        # # 给session设置cookie
        # session.cookies.update(cookie_to_dict(cookie))
        # page的url
        page_url = "http://mxjz.52jhxinxin.com/admin_agent/mySCustomerList"
        # 设置头部
        headers = {
            'Cookie': 'session=.eJw9j71qwzAUhV-l3NmDI9uhMWRTY2K41yRIFVdLoLZTW5YJOE1LFPLuFR26neE7fw84nZf-OkD5tdz6BE5jB-UDXj6ghMZwzsp7DvuCjZ1RtsJWNGIVdaCZghYoj57cMLPQGc_kOJC3SqdW1ZOV9UTikKOonZW7MXJTU8VMgSkJDui6kQym1mBuZZuR2nmea99ILtjtA4njROatwHAoSL3HHi0it0KHdzI0kNFZo_iHKr2FZwK3a7_87YfVZr3J1q-QwHe_jOd7e-n6_1skLgV_bqPl-QvrWVDC.DxnJHg.6cygbVeCttVwI7GZLod5uC5WT3k',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }
        form = {
            'page': '1',
            'agentid': self.chennel_id,
            'startTime': str(int(time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S")))),
            'endTime': str(int(time.mktime(time.strptime(f"{self.tomorrow} 00:00:00", "%Y-%m-%d %H:%M:%S"))))
        }
        # 访问url
        response = session.post(page_url, headers=headers, data=form)
        # 获取html
        info = response.json()['body']
        # 最终结果
        result = {
            "注册人数": info['total'],
            "实名人数": "null",
            "申请人数": 'null',
            "放款人数": 'null',
            "备注": ""
        }
        self.write_sql(result)


SH = {
    "login_url": "",
    "area": "",
    "product": "萌新记账",
    "username": "",
    "password": "",
    "channel": "",
    "id": "1969368"
}


all_local = [SH]

while True:
    for each in all_local:
        YQS(each).get_info()
    time.sleep(600)










