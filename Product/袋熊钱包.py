#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/18 0018 17:35 
# @Author : Chihiro 
# @Site :  
# @File : 袋熊钱包.py 
# @Software: PyCharm



import re
from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
import time
import warnings
from scrapy import Selector
import json
import pymysql
import json
from time import sleep
from tool.OCR import ocr
from cut_img import cut_img
from selenium.webdriver import Chrome
from datetime import datetime, date, timedelta
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class BJZ(BaseSpider):
    def __init__(self, account):
        super(BJZ, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="login"]/form/div/input[1]',
            "password": '//*[@id="login"]/form/div/input[2]',
            "login_button": '//*[@id="login"]/form/button',
            "check_code": "",
            "code_image_url": "",
            "success_ele": ""
        }
        # 模拟浏览器
        browser = Chrome()
        browser.minimize_window()
        # 登录url
        login_url = self.login_url
        # 进入登录页面
        browser.get(login_url)
        sleep(5)
        # 获取帐号+密码
        username = browser.find_element_by_xpath(xpath_info["username"])
        password = browser.find_element_by_xpath(xpath_info["password"])
        # 输入账号和密码
        username.send_keys(self.user_name)
        password.send_keys(self.password)
        # 登录
        browser.find_element_by_xpath(xpath_info["login_button"]).click()
        sleep(3)
        # 获取Cookie信息

        num = browser.find_element_by_xpath('//*[@id="channelloan"]/div/div/div[3]/span').text
        # 退出浏览器
        browser.quit()
        result = {
            "注册人数": num,
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": ''
        }
        self.write_sql(result)


SH = {
    "login_url": 'https://toupin.cn/web/channel/',
    "area": "",
    "product": "袋熊钱包",
    "username": "dxsfd14",
    "password": "123456",
    "channel": ""
}


all_local = [SH]


while True:
    for each in all_local:
        BJZ(each).get_info()
    time.sleep(1200)
