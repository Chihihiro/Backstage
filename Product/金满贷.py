# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 21:56
# @Author  : 逗比i
# @Project : Backstage
# @File    : 抱金砖.py
# @Software: PyCharm
# @Describe:
import time
from requests import Session
from scrapy import Selector
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict


class YQS(BaseSpider):
    def __init__(self, account):
        super(YQS, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="main"]/div/div/div/div[2]/div/form/div[1]/div/div[1]/input',
            "password": '//*[@id="main"]/div/div/div/div[2]/div/form/div[2]/div/div[1]/input',
            "login_button": '//*[@id="main"]/div/div/div/div[2]/div/form/div[5]/div/button',
            "check_code": '//*[@id="main"]/div/div/div/div[2]/div/form/div[4]/div/div[1]/input',
            "code_image_url": '//*[@id="s-canvas"]',
            "success_ele": '//span[@class="ivu-breadcrumb-item-link"]'
        }
        # 设置session
        session = Session()
        # 获取cookie
        token = self.check_get_token(xpath_info, (425, 435, 547, 469), "10400", "bearerToken")
        # # 给session设置cookie
        # session.cookies.update(cookie_to_dict(cookie))
        # page的url
        page_url = f"http://timedata.dgliao.cn/api/Bussiness/GetPartyBAccountData?PartyBId=1172&StartTime=2019-1-9&EndTime=2019-1-9&Limit=10&Offset=0&format=json"
        # 设置头部
        headers = {
            "Authorization": f"""Bearer {token.replace('"', "")}""",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }
        # 访问url
        response = session.get(page_url, headers=headers)
        # 获取html
        info = response.json()['rows'][0]
        # 最终结果
        result = {
            "注册人数": info['uploadCount'],
            "实名人数": "null",
            "申请人数": 'null',
            "放款人数": 'null'
        }
        print(result)
        # self.write_sql(result)


SH = {
    "login_url": "http://jiujidata.lyqchain.cn/#/login",
    "area": "上海",
    "product": "金满贷",
    "username": "jmm601",
    "password": "123456",
    "channel": "",
    "id": ""
}

all_local = [SH]

while True:
    for each in all_local:
        YQS(each).get_info()
    time.sleep(1200)










