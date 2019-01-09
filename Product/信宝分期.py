# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 21:56
# @Author  : 逗比i
# @Project : Backstage
# @File    : 抱金砖.py
# @Software: PyCharm
# @Describe:

from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
import time
import warnings


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
        url = f"https://api.fzxfenqi.com/dkcsdrainage/getInfoDrainage?pageSize=10&pageNo=1&channel=mlh&beginTime={self.today}&endTime={self.today}&channelsCode=2&_={time.time()*1000}"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 过滤警告信息
        warnings.filterwarnings("ignore")
        # 访问url
        response = session.get(url, headers=headers, verify=False)
        json_info = response.json()["result"][0]

        result = {
            "注册人数": json_info["registUsersNumber"],
            "实名人数": "null",
            "申请人数": json_info["applyLoanNumber"],
            "放款人数": "null"
        }
        self.write_sql(result)


SH = {
    "login_url": 'https://api.fzxfenqi.com/user/login',
    "area": "上海",
    "product": "信宝分期",
    "username": "mlh2",
    "password": "mlh2@123456",
    "channel": ""
}
SP = {
    "login_url": 'https://api.fzxfenqi.com/user/login',
    "area": "四平",
    "product": "信宝分期",
    "username": "mlh",
    "password": "mlh@123456",
    "channel": ""
}



all_local = [SH]



while True:
    for each in all_local:
        BJZ(each).get_info()
    time.sleep(600)










