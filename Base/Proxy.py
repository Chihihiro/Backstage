# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2019年01月10日 11:11
# @Author  : Joyce
# @Project : GanJi
# @File    : Proxy.py
# @Software: PyCharm
# @Describe: 

import requests


def get_proxy():
    # ip接口
    url = "http://api.ip.data5u.com/dynamic/get.html?order=6a1f20e0bc74d19794a6b3d2df4a6107&sep=3"
    # 请求接口
    response = requests.get(url)
    return response.text


























