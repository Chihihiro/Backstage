#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/4 0004 14:11 
# @Author : Chihiro 
# @Site :  
# @File : 百度.py 
# @Software: PyCharm

import requests
import json
from time import sleep, time
from tool.DealWithCookie import cookie_to_dict
from selenium.webdriver import Chrome
from urllib import request
from datetime import datetime, date, timedelta
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from tool.OCR import ocr
import pymysql
from cut_img import cut_img

browser = Chrome()
browser.maximize_window()
# 登录url
login_url = 'https://account.geetest.com/login/'
# 进入登录页面
browser.get(login_url)
sleep(5)
# 获取帐号+密码
username = browser.find_element_by_id('email')
password = browser.find_element_by_id('password')
# 输入账号和密码
username.send_keys('632207812@qq.com')
password.send_keys('chihiro123')
# 登录
browser.find_element_by_class_name('geetest_radar_tip_content').click()
sleep(2)

cookie = browser.get_cookies()
print(cookie)
cookie_dict = cookie_to_dict(cookie)

url = "https://account.geetest.com/api/initcaptcha"
info = requests.get(url).json()["data"]
timestamp = int(time()) * 1000
print(info)
url2 = f"https://api.geetest.com/get.php?is_next=true&type=slide3&gt={info['gt']}&challenge={info['challenge']}&lang=zh-cn&https=false&protocol=https%3A%2F%2F&offline=false&product=embed&api_server=api.geetest.com&isPC=true&width=100%25&callback=geetest_{timestamp}"
s = requests.Session()
s.cookies.update(cookie_dict)
r1 = s.get(url2).text.strip(f"geetest_{timestamp}()")
result = json.loads(r1)
print(result)
sleep(60)

# browser.find_element_by_xpath('//*[@id="base"]/div[2]/div/div/div[3]/div/form/div[5]/div/button').click()
# sleep(7)
# # 获取Cookie信息
# cookies = browser.get_cookies()