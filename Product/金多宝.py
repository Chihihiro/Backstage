#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/16 0016 13:11 
# @Author : Chihiro 
# @Site :  
# @File : 金多宝.py
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
            "password": '//*[@id="main"]/div/div/div/div[2]/div/form/div[4]/div/div/input',
            "login_button": '//*[@id="main"]/div/div/div/div[2]/div/form/div[5]/div/button',
            "check_code": '//*[@id="main"]/div/div/div/div[2]/div/form/div[3]/div/div/input',
            "code_image_url": '//*[@id="s-canvas"]',
            "success_ele": '//*[@id="main"]/div/div[1]/div/div[3]/div/div/div/div/a/span'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (366, 364, 512, 405), "10400")
        # 将cookie设置给session
        session.cookies.update(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        # page_url = f"http://0v10.cn/admin/customer/promote.html?start_time={self.today.year}%2F{str(100+int(self.today.month))[1:]}%2F{str(100+self.today.day)[1:]}+-+{self.tomorrow.year}%2F{str(100+int(self.tomorrow.month))[1:]}%2F{str(100+self.tomorrow.day)[1:]}"
        page_url = f"http://timedata.dgliao.cn/api/Bussiness/GetPartyBAccountData?PartyBId=381&StartTime={self.today}&EndTime={self.today}&format=json"
        print(page_url)
        # 请求url
        response = session.get(page_url, headers=headers)
        # 构造Selector
        info = response.json()

        # 获取数据
        print(info)
        # 获取结果
        # result = {
        #     "注册人数": info,
        #     "实名人数": "null",
        #     "申请人数": "null",
        #     "放款人数": "null",
        #     '备注':''
        # }
        # self.write_sql(result)
        # print(result)


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




