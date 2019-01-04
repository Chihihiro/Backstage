#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/2 0002 11:19 
# @Author : Chihiro 
# @Site :  
# @File : 解密.py 
# @Software: PyCharm

from urllib import request


msg = "%22%3A%22%22%2C%22"
name = "张"

print(request.unquote(msg))
print(request.quote(name))


