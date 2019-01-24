#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/22 0022 15:26 
# @Author : Chihiro 
# @Site :  
# @File : 钱包到.py 
# @Software: PyCharm






from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
from scrapy import Selector
from time import sleep
import json
from selenium.webdriver import Chrome
import re


class XHY(BaseSpider):
    def __init__(self, account):
        super(XHY, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="app"]/div/div/div[2]/form/div[1]/div/div/input',
            "password": '//*[@id="app"]/div/div/div[2]/form/div[2]/div/div/input',
            "login_button": '//*[@id="app"]/div/div/div[2]/form/div[3]/button',
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
        num = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/div[2]/div/div[1]/span[2]').text

        # 退出浏览器
        browser.quit()
        # print(num)
        # 获取结果
        result = {
            "注册人数": re.search('(\d+)', num).group(1),
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            '备注': ''
        }
        self.write_sql(result)


SH = {
    "login_url": "http://dailibao-admin.kongapi.com/login",
    "area": "",
    "product": "钱包到",
    "username": "QBD_KLSQ",
    "password": "123456",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        XHY(each).get_info()
        sleep(600)