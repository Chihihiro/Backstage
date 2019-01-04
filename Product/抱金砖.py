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


class BJZ(BaseSpider):
    def __init__(self, account):
        super(BJZ, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="app"]/div/form/div[1]/div/div[1]/input',
            "password": '//*[@id="app"]/div/form/div[2]/div/div[1]/input',
            "login_button": '//*[@id="app"]/div/form/div[3]/div/button',
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
        json_url = f"http://crm.channel.51zhihe.com/backend/statistics?page=1&data=%7B%22search%22:%7B%22start%22:%22{self.today}%22,%22end%22:%22{self.today}%22,%22name%22:%22%22%7D%7D"
        # 设置头部
        headers = {
            "Host": f"{cookie[0]['domain']}",
            "Referer": f"http://{cookie[0]['domain']}/backend/index",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 访问url
        response = session.get(json_url, headers=headers)

        # 获取数据
        json_info = response.json()["data"]["lists"]["data"][0]
        # 最终结果
        result = {
            "注册人数": json_info["registers"],
            "实名人数": "null",
            "申请人数": json_info["applications"],
            "放款人数": "null"
        }
        self.write_sql(result)


SH = {
    "login_url": "http://crm.channel.51zhihe.com/#/",
    "area": "上海",
    "product": "抱金砖",
    "username": "rj163",
    "password": "123456abc",
    "channel": ""
}
WD = {
    "login_url": "http://crm.channel.51zhihe.com/#/",
    "area": "外地",
    "product": "抱金砖",
    "username": "RJ123",
    "password": "123456ABC",
    "channel": ""
}
SP = {
    "login_url": "http://crm.channel.51zhihe.com/#/",
    "area": "四平",
    "product": "抱金砖",
    "username": "rj219",
    "password": "123456abc",
    "channel": ""
}


all_local = [SH, WD, SP]
for each_local in all_local:
    spider = BJZ(each_local)
    spider.get_info()











