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
            'Cookie': 'session=.eJw9j71ugzAUhV-lujMDMTCAlM0NCtK9iMiudb1EKhCBMa1EmlZxlHev1aHbGb7z94DzZRuvE1Rf221M4DwPUD3g5R0qaA3nrLzncCzY2BVlL2xNM9ZRB1opaIHy5MlNKwud8UqOA3mrdGpVs1jZLCS6HEXjrDzMkVvaOmYKTElwQDfMZDC1BnMr-4zUwfPa-FZywe4YSJwWMq8Fhq4g9RZ7tIjcDh3eydBERmet4h-q9R6eCdyu4_a3H3aiLAtRQgLf4zZf7v3nMP7f6j-ajLp9tDx_AeupUMY.Dwce-w.KSw8gNZJGTS9pk2SQKsSdHXjb8Y',
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
            "放款人数": 'null'
        }
        self.write_sql(result)


SH = {
    "login_url": "http://jlg.lkdjhls.cn/admin/jlg.html#/sign-in",
    "area": "上海",
    "product": "金来购",
    "username": "hzz397",
    "password": "123456",
    "channel": "",
    "id": "1299534"
}
WD = {
    "login_url": "http://jlg.lkdjhls.cn/admin/jlg.html#/sign-in",
    "area": "外地",
    "product": "金来购",
    "username": "hzz935",
    "password": "123456",
    "channel": "",
    "id": "1299524"
}
SP = {
    "login_url": "http://jlg.lkdjhls.cn/admin/jlg.html#/sign-in",
    "area": "四平",
    "product": "金来购",
    "username": "hzz396",
    "password": "123456",
    "channel": "",
    "id": "1299529"
}

all_local = [SH, WD, SP]

while True:
    for each in all_local:
        YQS(each).get_info()
    time.sleep(1200)










