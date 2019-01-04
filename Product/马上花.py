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
            "username": '//*[@id="UserName"]',
            "password": '//*[@id="UserPsd"]',
            "login_button": '//*[@id="FF"]/div[3]/div[2]/div/div[4]/div[3]',
            "check_code": '//*[@id="Code"]',
            "code_image_url": '//*[@id="imgValidateCode"]',
            "success_ele": '/html/body/div[1]/div/div/div[1]/img'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (743, 449, 846, 489), "10400")
        # 将cookie设置给session
        session.cookies.update(cookie_to_dict(cookie))

        json_url = "http://msh.mrxds.pw/admin.php/Members/Tuiguangtj/DataList"
        # 请求url
        # 设置头部信息
        # print(cookie)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }
        # print(headers)
        response = session.post(json_url, headers=headers)
        # print(response)
        # 构造Selector
        # selector = Selector(text=response.text)
        # print(response.text)
        json = response.json()["rows"][0]
        # 获取数据
        # info = selector.xpath('//*[@id="bigDataList"]/tbody/tr/td/text()').extract()
        # print(info)
        # # 获取结果
        result = {
            "注册人数": json['Regists'],
            "实名人数": "null",
            "申请人数": json['Applynumbs'],
            "放款人数": json['Downs']
        }
        self.write_sql(result)
        # print(result)


SH = {
    "login_url": "http://msh.mrxds.pw/admin/System/Login/login",
    "area": "外地",
    "product": "马上花",
    "username": "tuiguang27",
    "password": "a123456",
    "channel": ""
}


all_area = [SH]


all_local = [SH]
for each_local in all_local:
    spider = XHY(each_local)
    spider.get_info()













