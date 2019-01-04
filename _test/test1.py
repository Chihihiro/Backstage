#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/12/28 0028 10:19 
# @Author : Chihiro 
# @Site :  
# @File : test1.py 
# @Software: PyCharm



from requests import Session
import time
import json


session = Session()
# 设置头部信息
headers = {
    # "Content-Type": "application/json; charset=utf-8",
    # "accessToken": "cede704783b05eeb72631e2b1ae0b617",
    # "Origin": "http://wxqz.zaixianjieshu.com",
    # "Referer": "http://wxqz.zaixianjieshu.com/wxqz/H5/flowAdmin/index.html",
    "accept": "application/json, text/javascript, */*; q=0.",
    "cookie": "PHPSESSID=33dbp2fde9mg3v02vfq4jv4dj0",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
    # "Access-Control-Allow-Headers": 'Content-Type,Accept,X-Requested-With,remember-me,bid,accessToken,productCategory,appCode'
}
# 页面url
page_url = "https://www.gglcqm.cn/admin/channel/counts/ids/83?addtabs=1"
# post参数
form = {
    'page': '1',
    'agentid': '30656672',
    # 'startTime': str(int(time.mktime(time.strptime(f"{self.today} 00:00:00", "%Y-%m-%d %H:%M:%S")))),
    # 'endTime': str(int(time.mktime(time.strptime(f"{self.tomorrow} 00:00:00", "%Y-%m-%d %H:%M:%S"))))
    # 'startTime':'1546358400'
}

# 请求url
response = session.get(page_url, headers=headers)
# 获取html
# info = response.json()

print(response.text)
