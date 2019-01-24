#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/21 0021 17:16 
# @Author : Chihiro 
# @Site :  
# @File : 天猫易贷.py 
# @Software: PyCharm




from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep
import re



class XHY(BaseSpider):
    def __init__(self, account):
        super(XHY, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '/html/body/div/div/div/div[2]/div[1]/input',
            "password": '/html/body/div/div/div/div[2]/div[2]/input',
            "login_button": '/html/body/div/div/div/div[2]/button',
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.no_check_get_cookie(xpath_info)
        # 将cookie设置给session
        session.cookies.update(cookie_to_dict(cookie))
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 页面url
        url = f"https://saas.fin-tech.cn/admin/index.php/linkshare/index/share_count_ajax.html?page=1&limit=10&search_date_start={self.today}&search_date_end={self.today}"
        # 请求url

        response = session.get(url, headers=headers)
        # 构造Selector
        print(response.json())
        info = response.json()['data']['0']
        zc = re.sub("\D", "", info["count"])
        # 获取结果
        result = {
            "注册人数": zc,
            "实名人数": "null",
            "申请人数": info['submit_count'],
            "放款人数": "null",
            '备注':''
        }
        self.write_sql(result)


SH = {
    "login_url": "https://saas.fin-tech.cn/admin/index.php?g=linkshare&m=index",
    "area": "",
    "product": "天猫易贷",
    "username": "qw1234",
    "password": "qw1234",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        XHY(each).get_info()
        sleep(1200)