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
            "username": '//*[@id="app"]/div/div/div/div[2]/form/div[1]/div/div/input',
            "password": '//*[@id="app"]/div/div/div/div[2]/form/div[2]/div/div/input',
            "yan": '//*[@id="app"]/div/div/div/div[2]/form/div[3]/div/div/input',
            "login_button": '//*[@id="app"]/div/div/div/div[2]/form/div[4]/button',
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
        yan = browser.find_element_by_xpath(xpath_info["yan"])
        # 输入账号和密码
        username.send_keys(self.user_name)
        password.send_keys(self.password)
        yan.send_keys('0000')
        # 登录
        browser.find_element_by_xpath(xpath_info["login_button"]).click()
        sleep(3)
        browser.find_element_by_xpath('//*[@id="sidebar"]/div/div[1]/div/div/ul/li[2]/div').click()
        sleep(2)
        browser.find_element_by_xpath('//*[@id="sidebar"]/div/div[1]/div/div/ul/li[2]/ul/li/span').click()
        sleep(2)
        # day1 = browser.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[2]/div/form/div[1]/div/div[1]/div/input')
        # day2 = browser.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[2]/div/form/div[1]/div/div[3]/div/input')
        # day1.send_keys(f"{self.today}")
        # day2.send_keys(f'{self.today}')
        browser.find_element_by_xpath('//*[@id="app"]/div/div[3]/div[2]/div/form/div[3]/div/button').click()
        sleep(3)
        cookies = browser.get_cookies()
        print(cookies)
        # # 退出浏览器
        # browser.quit()
        #
        # # 设置session
        # session = Session()
        # # session.cookies.update(cookie_to_dict(cookies))
        # headers = {
        # "Cookie": "JSESSIONID=a25e7f0b-2c06-4be5-b185-4b607013fa78",
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        # }
        # url = f'https://jxh.fengxingweb.com/man/extension/data/count?beginTime={self.today}&endTime={self.today}&status=1'
        # response = session.get(url, headers=headers)
        #
        #
        # info = response.json()['object'][0]
        # # 获取结果
        # result = {
        #     "注册人数": info['registerCount'],
        #     "实名人数": info['realNameCount'],
        #     "申请人数": info['applyCount'],
        #     "放款人数": info['makeSuccessCount'],
        #     '备注': ''
        # }
        # self.write_sql(result)


SH = {
    "login_url": "https://jxh.fengxingweb.com/#/login",
    "area": "",
    "product": "今享花",
    "username": "jxh02",
    "password": "123123",
    "channel": ""
}


all_area = [SH]

while True:
    for each in all_area:
        XHY(each).get_info()
        sleep(600)