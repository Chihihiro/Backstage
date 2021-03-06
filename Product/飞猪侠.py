#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/3 0003 17:06 
# @Author : Chihiro 
# @Site :  
# @File : 爱卡钱包.py 
# @Software: PyCharm



from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep
import time


class DRB(BaseSpider):

    def __init__(self, account):
        super(DRB, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="account"]',
            "password": '//*[@id="password"]',
            "login_button": '//*[@id="root"]/div/div/div[2]/div/form/div[4]/div/div/span/button',
            "check_code": '//*[@id="imgCode"]',
            "code_image_url": '//*[@id="root"]/div/div/div[2]/div/form/div[3]/div/div/span/div/div[2]/img',
            "success_ele": '//*[@id="root"]/div/div/div[1]/div/div/span/span'
        }
        # 获取cookie
        token = self.check_get_token(xpath_info, (565, 352, 653, 385), "30400", 'accessToken')
        # 设置session
        session = Session()
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
            "accessToken": token,
        }
        # 页面url
        json_url = "http://101.37.191.117:3001/channel/admin/data"
        args = {
            'channelCode': self.channel,
            'merchantId': "0",
            'registerBeginDate': int(
                time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S"))) * 1000,
            'registerEndDate': int(
                time.mktime(time.strptime(f"{self.tomorrow} 00:00:00", "%Y-%m-%d %H:%M:%S"))) * 1000
        }
        # 请求url
        response = session.post(json_url, headers=headers, json=args)
        info = response.json()['data']['channelDataList'][0]
        # 获取结果
        print(info)
        result = {
            "注册人数": info['registerCount'],
            "实名人数": "null",
            "申请人数": info['applyCount'],
            "放款人数": info['loanCount'],
            "备注": ""
        }
        print(result)
        self.write_sql(result)




SH = {
    "login_url": "http://tslj.zaixianjieshu.com/tslj/H5/flowAdmin/index.html#/user/login",
    "area": "",
    "product": "飞猪侠",
    "username": "cwt",
    "password": "cwt123",
    "channel": "2019012200OWBXT"
}


all_area = [SH]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(1200)



