# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 21:56
# @Author  : 逗比i
# @Project : Backstage
# @File    : 抱金砖.py
# @Software: PyCharm
# @Describe:
import re
from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
import time

class BJZ(BaseSpider):
    def __init__(self, account):
        super(BJZ, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '/html/body/div/div/div/div[2]/div[1]/input',
            "password": '/html/body/div/div/div/div[2]/div[2]/input',
            "login_button": '/html/body/div/div/div/div[2]/button',
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
        json_url = f"https://saas.fin-tech.cn/admin/index.php/linkshare/index/share_count_ajax.html?page=1&limit=10&search_date_start={self.today}&search_date_end={self.today}"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 访问url
        response = session.get(json_url, headers=headers)

        # 获取数据
        json_info = response.json()["data"]["0"]
        # 最终结果
        zc = re.sub("\D", "", json_info["count"])
        result = {
            "注册人数": zc,
            "实名人数": "null",
            "申请人数": json_info["submit_count"],
            "放款人数": "null"
        }
        self.write_sql(result)


WD = {
    "login_url": "https://saas.fin-tech.cn/admin/index.php?g=linkshare&m=index",
    "area": "外地",
    "product": "趣花呗",
    "username": "hh7",
    "password": "qwe123",
    "channel": ""
}

SH = {
    "login_url": "https://saas.fin-tech.cn/admin/index.php?g=linkshare&m=index",
    "area": "上海",
    "product": "趣花呗",
    "username": "py114",
    "password": "qwe123",
    "channel": ""
}

SP = {
    "login_url": "https://saas.fin-tech.cn/admin/index.php?g=linkshare&m=index",
    "area": "四平",
    "product": "趣花呗",
    "username": "py104",
    "password": "qwe123",
    "channel": ""
}



all_local = [SH, WD, SP]

while True:
    for each in all_local:
        BJZ(each).get_info()
    time.sleep(1200)










