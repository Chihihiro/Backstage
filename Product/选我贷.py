#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/21 0021 16:10 
# @Author : Chihiro 
# @Site :  
# @File : 选我贷.py 
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
            "username": '//*[@id="main"]/div/div/div/div[2]/div/form/div[1]/div/div/input',
            "password": '//*[@id="main"]/div/div/div/div[2]/div/form/div[2]/div/div/input',
            "login_button": '//*[@id="main"]/div/div/div/div[2]/div/form/div[5]/div/button',
            "check_code": '//*[@id="main"]/div/div/div/div[2]/div/form/div[4]/div/div/input',
            "code_image_url": '//*[@id="s-canvas"]',
            "success_ele": '//*[@id="main"]/div/div[2]/div/div/div/div[2]/div/div/div/div[1]'
        }
        # 设置session
        session = Session()
        # 获取cookie
        token = self.check_get_token(xpath_info, (697, 443, 885, 477), "10400", "bearerToken")
        # 设置头部信息
        headers = {
            "Authorization": f"""Bearer {token.replace('"', "")}""",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        print(headers)
        # 页面url
        page_url = f'http://timedata.dgliao.cn/api/Bussiness/GetPartyBAccountData?PartyBId=304&StartTime=2018-12-23&EndTime={self.today}&Limit=10&Offset=0&format=json'
        # 请求url
        response = session.get(page_url, headers=headers)
        # 获取数据
        info = response.json()
        # info = response.text#json()["todayRegCount"]
        # print(info)
        # print(response.status_code)
        # 获取结果
        result = {
            "注册人数": info["rows"][0]["uploadCount"],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            '备注':''
        }
        self.write_sql(result)
        # print(result)


SH = {
    "login_url": "http://justc.qkjinrong.cn/#/login",
    "area": "",
    "product": "选我贷",
    "username": "rong0396",
    "password": "rong0396",
    "channel": ""
}


all_area = [SH]


for each in all_area:
    XHY(each).get_info()
    sleep(1200)




