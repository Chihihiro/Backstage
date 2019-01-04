#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/4 0004 14:11 
# @Author : Chihiro 
# @Site :  
# @File : 百度.py 
# @Software: PyCharm


from selenium.webdriver import Chrome
from time import sleep

driver = Chrome()
driver.get("http://www.baidu.com")
sleep(3)

info = driver.execute_script("var i=0; i++; return i")
print(info)

