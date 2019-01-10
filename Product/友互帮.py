#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/10 0010 12:40 
# @Author : Chihiro 
# @Site :  
# @File : 友互帮.py 
# @Software: PyCharm



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
            "username": '//*[@id="code"]',
            "password": '//*[@id="channelPassword"]',
            "login_button": '//*[@id="root"]/div/div/form/div[3]/div/div/button',
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
        url = "http://c.ypuzhen.com/web/clUser/selectListAll"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }

        form = {
            'pageNum': 1,
            'pageSize': 2000,
            'channelId': 284,
            'startTime': f'{self.today}',
            'endTime': f'{self.today}',
        }
        # 访问url
        response = session.post(url, headers=headers, data=form)
        json_info = response.json()['data']['pageDto']
        #计算实名人数
        num = json_info['list']
        real_name = []
        for i in num:
            name = i['realName']
            if name:
                real_name.append(name)

        result = {
            "注册人数": json_info["total"],
            "实名人数": len(real_name),
            "申请人数": "null",
            "放款人数": "null"
        }
        self.write_sql(result)


SH = {
    "login_url": 'http://c.ypuzhen.com/#/AppLogin',
    "area": "",
    "product": "友互帮",
    "username": "ju003",
    "password": "123456",
    "channel": ""
}




all_local = [SH]



while True:
    for each in all_local:
        BJZ(each).get_info()
    time.sleep(600)
