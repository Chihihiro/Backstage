#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2019/1/10 0010 12:22
# @Author : Chihiro
# @Site :
# @File : 金来购2.py
# @Software: PyCharm


import time
from requests import Session
from scrapy import Selector
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict


class YQS(BaseSpider):
    def __init__(self, account):
        super(YQS, self).__init__(account)
        self.chennel_id = account["id"]

    def get_info(self):
        # xpath_info = {
        #     "username": '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[1]/form/div[1]/div/div/input',
        #     "password": '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[1]/form/div[2]/div/div[1]/input',
        #     "login_button": '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[1]/div',
        #     "check_code": '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[1]/form/div[3]/div/div/input',
        #     "code_image_url": '//*[@id="app"]/div/div/div[2]/div[2]/div[2]/div[1]/form/div[3]/div/img',
        #     "success_ele": '//*[@id="app"]/div/div[1]/div[3]/div/ul/li[1]/div'
        # }
        # 设置session
        session = Session()
        # 获取cookie
        # cookie = self.check_get_cookie(xpath_info, (535, 378, 615, 408), "30400")
        # # 给session设置cookie
        # session.cookies.update(cookie_to_dict(cookie))
        # page的url
        page_url = "http://jlg.lkdjhls.cn/admin_agent/mySCustomerList"
        # 设置头部
        headers = {
            'Cookie': 'session=.eJw9j81qg0AUhV-l3LULnWgKQnbTSIR7JWGm0zubQNWg40jBNA1OyLt36KK7s_jO3wPOl6W_DlB-L7c-gfPYQfmAl08ooTGcs_Kew6FgY2eUrbAVjVhFHWimoAXKkyc3zCz0hmdyHMhbpVOr6snKeiJxzFHUzsr9GLmpqWKmwJQEB3TdSAZTazC3st2Q2nuea99ILtgdAonTROatwHAsSL3HHi0il6HDlQwNZPSmUXynSu_gmcDt2i9_-yHLtq_FNocEfvplvKztV9f_32o_aOX7Llqev-1RUSQ.Dxhaxw.lVOhwqkvCaP4HhZC2zbScQd5-Hg',
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
        }
        form = {
            'page': '1',
            'agentid': self.chennel_id,
            'startTime': str(int(time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S")))),
            'endTime': str(int(time.mktime(time.strptime(f"{self.tomorrow} 00:00:00", "%Y-%m-%d %H:%M:%S"))))
        }
        # 访问url
        response = session.post(page_url, headers=headers, data=form)
        # 获取html
        info = response.json()['body']
        # 最终结果
        result = {
            "注册人数": info['total'],
            "实名人数": "null",
            "申请人数": 'null',
            "放款人数": 'null',
            "备注": "null"
        }
        self.write_sql(result)


SH = {
    "login_url": "",
    "area": "",
    "product": "金来购2",
    "username": "",
    "password": "",
    "channel": "",
    "id": "1167564"
}


all_local = [SH]

while True:
    for each in all_local:
        YQS(each).get_info()
    time.sleep(1200)










