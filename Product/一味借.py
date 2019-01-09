#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/8 0008 16:06 
# @Author : Chihiro 
# @Site :  
# @File : 一味借.py 
# @Software: PyCharm


from selenium import webdriver
from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
import json
from time import sleep
class BJZ(BaseSpider):
    def __init__(self, account):
        super(BJZ, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="app"]/div/form/div[1]/div/div/input',
            "password": '//*[@id="app"]/div/form/div[2]/div/div[1]/input',
            "login_button": '//*[@id="app"]/div/form/div[3]/div/button',
            "check_code": "",
            "code_image_url": "",
            "success_ele": ""
        }
        # 设置session
        session = Session()
        # 获取cookie
        # cookie = self.no_check_get_cookie(xpath_info)
        browser = webdriver.Chrome()
        browser.maximize_window()
        # 登录url
        # 进入登录页面
        browser.get(self.login_url)
        sleep(5)
        # 获取帐号+密码
        username = browser.find_element_by_xpath(xpath_info["username"])
        password = browser.find_element_by_xpath(xpath_info["password"])
        # 输入账号和密码
        username.send_keys(self.user_name)
        password.send_keys(self.password)
        # 登录
        browser.find_element_by_xpath(xpath_info["login_button"]).click()
        sleep(7)
        browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[1]/div/ul/div/li/div/span').click()
        sleep(3)
        browser.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[1]/div/ul/div/li/ul/a/li/span').click()
        sleep(5)
        info = browser.find_element_by_xpath('//*[@id="app"]/div/div[2]/section/div/div[1]/div[3]/table/tbody/tr/td[3]').text
        # # 设置头部
        browser.quit()
        result = {
            "注册人数": info,
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null"
        }
        self.write_sql(result)


SH = {
    "login_url": "http://nmc-admin.51yunpos.shop/#/login?redirect=%2Fhome",
    "area": "",
    "product": "一味借",
    "username": "18656783389",
    "password": "123456",
    "channel": ""
}


all_local = [SH]
for each_local in all_local:
    spider = BJZ(each_local)
    spider.get_info()
