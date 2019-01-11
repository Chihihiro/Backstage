#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/11 0011 9:45 
# @Author : Chihiro 
# @Site :  
# @File : 钱包借3.py
# @Software: PyCharm



from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from time import sleep


class BJZ(BaseSpider):
    def __init__(self, account):
        super(BJZ, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="form"]/div[1]/input',
            "password": '//*[@id="form"]/div[2]/input',
            "login_button": '//*[@id="form"]/div[3]/input',
            "check_code": "",
            "code_image_url": "",
            "success_ele": ""
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.no_check_get_cookie(xpath_info)
        # 给session设置cookie
        session.cookies.update(cookie_to_dict(cookie))
        # json的url
        json_url = f"https://mmfqadmin.358fintech.com/drainage/getDrainageInfoListByPartner?pageSize=10&pageNum=0&startDate={self.today}&endDate={self.today}&channelsCode=2&_=1547003414269"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 访问url
        response = session.get(json_url, headers=headers)
        # 获取数据
        json_info = response.json()["result"][0]
        # 最终结果
        result = {
            "注册人数": json_info["channelsShowNumber"],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": ""
        }
        # print(result)
        self.write_sql(result)


SP = {
    "login_url": "https://mmfqadmin.358fintech.com/user/login;JSESSIONID=439ae0e3-44c2-4cec-a31b-a6ba11538cd9",
    "area": "",
    "product": "钱包借3",
    "username": "qyh",
    "password": "qyh123",
    "channel": ""
}


while True:
    all_local = [SP]
    for each_local in all_local:
        spider = BJZ(each_local)
        spider.get_info()
    sleep(600)










