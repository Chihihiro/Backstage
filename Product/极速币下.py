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
import json
import time
import http.cookiejar
import urllib.request, urllib.parse, urllib.error



def login():
    login_url = 'https://passport.jinfuzi.com/passport/user/doLogin.html'
    values = {'paramMap.password': '68125542', 'paramMap.userName': '15026588463'}
    postdata = urllib.parse.urlencode(values).encode()
    user_agent = r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'
    headers = {'User-Agent': user_agent}
    cookie_filename = 'cookie_jar.txt'
    cookie_jar = http.cookiejar.MozillaCookieJar(cookie_filename)
    handler = urllib.request.HTTPCookieProcessor(cookie_jar)
    opener = urllib.request.build_opener(handler)
    try:
        print('-------------')
        request = urllib.request.Request(login_url, data=postdata, headers=headers, method='POST')
        response = opener.open(request)
    except urllib.error.URLError as e:
        print(e.code, ':', e.reason)
    # cookie_jar.save(ignore_discard=True, ignore_expires=True)  # 保存cookie到cookie.txt中

    for item in cookie_jar:
        print('Name = ' + item.name)
        print('Value = ' + item.value)

        cook = item.value
        cookise = {'Cookie': cook}
        return cookise



class DRB(BaseSpider):
    def __init__(self, account):
        super(DRB, self).__init__(account)

    def get_info(self):
        # 设置session
        session = Session()
        # 设置头部信息
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
            'Host': 'merchant.xianjinxia.com',
            'loginToken': '28307fbeda88ea82e7401562460a72668f607836e344de926321f3abfd0b7e08054a9db9c98a93a73dcf9301409cf55694ad8f165fbf7a460123e97d6ae1e360',
            'Origin': 'http: // merchant.xianjinxia.com',
            'Referer': 'http: // merchant.xianjinxia.com /'
        }
        # 页面url
        json_url = "http://merchant.xianjinxia.com/api/v2/merchant/promotionStatistics/channel/thirdPage"
        args = {
            'dtEnd': int(time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S")))*1000,
            'dtStart': int(time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S")))*1000,
            'dtRange': [int(time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S")))*1000,
                        int(time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S")))*1000,]
        }
        # 请求url
        response = session.post(json_url, headers=headers, json=args)
        # info = response.json()
        # print(info)
        info = response.json()['data']['pageInfo']['list'][0]
        print(info)
        # 获取结果
        result = {
            "注册人数": info['regCount'],
            "实名人数": "null",
            "申请人数": 'null',
            "放款人数": 'null'
        }
        print(result)
        self.write_sql(result)


SH = {
    "login_url": '',
    "area": "上海",
    "product": "极速币下",
    "username": "",
    "password": "",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        DRB(each).get_info()
    sleep(1200)













