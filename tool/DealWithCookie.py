# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 21:14
# @Author  : 逗比i
# @Project : Backstage
# @File    : DealWithCookie.py
# @Software: PyCharm
# @Describe: 


# 将cookie转为字典格式
def cookie_to_dict(cookie_info):
    cookie_dict = {}
    for each in cookie_info:
        cookie_dict[each["name"]] = each["value"]
    return cookie_dict













