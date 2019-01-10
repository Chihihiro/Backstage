# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 21:56
# @Author  : 逗比i
# @Project : Backstage
# @File    : 抱金砖.py
# @Software: PyCharm
# @Describe:
import time
import json
from requests import Session
from scrapy import Selector
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict


class YQS(BaseSpider):
    def __init__(self, account):
        super(YQS, self).__init__(account)
        self.chennel_id = account["id"]

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="code"]',
            "password": '//*[@id="channelPassword"]',
            "login_button": '//*[@id="root"]/div/div/form/div[3]/div/div/button',
            "check_code": '',
            "code_image_url": '',
            "success_ele": ''
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.no_check_get_cookie(xpath_info)
        # 给session设置cookie
        session.cookies.update(cookie_to_dict(cookie))
        # page的url
        page_url = "http://xfshchannel.tgjrfw.com/web/clUser/selectListAll"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }
        form = {
            "pageNum": "1",
            "pageSize": "2000",
            "channelId": "396",
            "startTime": f"{self.today}",
            "endTime": f"{self.today}"
        }
        # 访问url
        response = session.post(page_url, headers=headers, data=form)
        info = response.json()["data"]["pageDto"]
        # 最终结果
        result = {
            "注册人数": info['total'],
            "实名人数": 0,
            "申请人数": 'null',
            "放款人数": 'null',
            "备注": ""
        }
        sm = info["list"]
        for each in sm:
            # print(each)
            if each["realName"]:
                result["实名人数"] += 1

        # print(result)
        self.write_sql(result)


WD = {
    "login_url": "http://xfshchannel.tgjrfw.com/#/AppLogin",
    "area": "外地",
    "product": "幸福生活",
    "username": "xs2",
    "password": "123456",
    "channel": "",
    "id": ""
}

all_local = [WD]

while True:
    for each in all_local:
        YQS(each).get_info()
    time.sleep(1200)










