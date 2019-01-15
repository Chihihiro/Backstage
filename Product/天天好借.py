#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2019/1/15 0015 12:28 
# @Author : Chihiro 
# @Site :  
# @File : 天天好借.py
# @Software: PyCharm





import re
from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
import time
import warnings
from scrapy import Selector
import json
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from datetime import datetime, date, timedelta
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities



class BJZ(BaseSpider):
    def __init__(self, account):
        super(BJZ, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="app"]/div/form/div[1]/div/div/input',
            "password": '//*[@id="app"]/div/form/div[2]/div/div/input',
            "login_button": '//*[@id="app"]/div/form/div[3]/div/button',
            "check_code": "",
            "code_image_url": "",
            "success_ele": ""
        }
        # 设置session
        session = Session()
        # 获取cookie
        # 模拟浏览器
        browser = Chrome()
        browser.maximize_window()
        # 登录url
        login_url = self.login_url
        # 进入登录页面
        browser.get(login_url)
        # 获取帐号+密码
        username = browser.find_element_by_xpath(xpath_info["username"])
        password = browser.find_element_by_xpath(xpath_info["password"])
        time.sleep(2)
        for i1 in range(10):
            username.send_keys(Keys.BACK_SPACE)
            password.send_keys(Keys.BACK_SPACE)
        time.sleep(5)
        # 输入账号和密码
        username.send_keys(self.user_name)
        password.send_keys(self.password)
        # 登录
        browser.find_element_by_xpath(xpath_info["login_button"]).click()
        time.sleep(7)
        # 获取Token
        token_field = '_CookieKEY_'
        js = f"var token=window.localStorage.{token_field}; return token"
        token = browser.execute_script(js)
        d = json.loads(token)
        value = json.loads(d["userinfo"]["value"])["sessionToken"]
        # 给session设置cookie
        session.cookies.update(cookie_to_dict(browser.get_cookies()))
        browser.quit()
        # json的url
        url = f"https://ohmyadmin.happycheer.com/api.php?route=Admin/getTableList&schemaKey=JGD_ADMIN_CHANNEL_JHI-USER_SELECT&page=1&count=10&sessionToken={value}"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        args = {
            "condition": json.dumps({
                "`jhi_user`.`channel`": "chipin05",
                "`jhi_user`.`ctime`": f"{self.today} 00:00:00|{self.tomorrow} 00:00:00"
            })
        }
        # 访问url
        response = session.post(url, headers=headers, data=args)
        info = response.json()["result"]
        print(info)
        result = {
            "注册人数": info["totalCount"],
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null",
            "备注": ''

        }
        self.write_sql(result)


SH = {
    "login_url": 'https://ohmyadmin.happycheer.com/login',
    "area": "",
    "product": "天天好借",
    "username": "chipin05",
    "password": "123456",
    "channel": ""
}


all_local = [SH]


while True:
    for each in all_local:
        BJZ(each).get_info()
    time.sleep(1200)
