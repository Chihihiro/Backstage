# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 20:20
# @Author  : 逗比i
# @Project : Backstage
# @File    : BaseSpider.py
# @Software: PyCharm
# @Describe: 爬虫基类

import pymysql
import json
from time import sleep
from tool.OCR import ocr
from cut_img import cut_img
from selenium.webdriver import Chrome
from datetime import datetime, date, timedelta
from selenium.common.exceptions import NoSuchElementException, UnexpectedAlertPresentException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

d = DesiredCapabilities.CHROME
d['loggingPrefs'] = { 'performance':'ALL' }


class BaseSpider:
    """
    主要功能:
    1)动态获取cookie信息
    2)将数据写入MySQL数据库中
    """
    # 各个属性
    def __init__(self, account):
        self.login_url = account["login_url"]  # 登录地址
        self.area = account["area"]  # 地区
        self.product = account["product"]  # 产品名称
        self.user_name = account["username"]  # 帐号
        self.password = account["password"]  # 密码
        self.now = datetime.now()  # 当前时间
        self.today = date.today()  # 今天日期
        self.channel = account["channel"]  # 渠道
        self.yesterday = str(self.today - timedelta(days=1))  # 昨天日期
        self.tomorrow = str(self.today + timedelta(days=1))  # 明天日期

    # 获取cookie
    def no_check_get_cookie(self, xpath_info):
        """
        xpath_info : 表单元素的xpath组成的字典
        xpath["username"] : 账号的xpath
        xpath["password"] : 密码的xpath
        xpath["login_button"] : 登陆按钮的xpath
        """
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
        sleep(7)
        # 获取Cookie信息
        cookies = browser.get_cookies()
        # 退出浏览器
        browser.quit()
        # 返回cookie信息
        return cookies

    def no_check_get_token(self, xpath_info, token_field):
        # 模拟浏览器
        browser = Chrome()
        browser.minimize_window()
        # 登录url
        login_url = self.login_url
        # 进入登录页面
        browser.get(login_url)
        # 获取帐号+密码
        username = browser.find_element_by_xpath(xpath_info["username"])
        password = browser.find_element_by_xpath(xpath_info["password"])
        # 输入账号和密码
        username.send_keys(self.user_name)
        password.send_keys(self.password)
        # 登录
        browser.find_element_by_xpath(xpath_info["login_button"]).click()
        sleep(7)
        # 获取Token
        js = f"var token=window.localStorage.{token_field}; return token"
        token = browser.execute_script(js)
        browser.quit()
        return token

    def check_get_cookie(self, xpath_info, img_size, image_type):
        """
        xpath_info : 表单元素的xpath组成的字典
        xpath["username"] : 账号的xpath
        xpath["password"] : 密码的xpath
        xpath["check_code"] : 验证码输入框的xpath
        xpath["code_image_url"] : 验证码图片img的xpath
        xpath["login_button"] : 登陆按钮的xpath
        xpath["success_ele"] : 登陆成功后的任意一个页面元素的xpath
        """
        # 模拟浏览器
        browser = Chrome()
        browser.minimize_window()
        # 登录url
        login_url = self.login_url
        # 进入登录页面
        browser.get(login_url)

        def login():
            # 获取帐号+密码
            username = browser.find_element_by_xpath(xpath_info["username"])
            password = browser.find_element_by_xpath(xpath_info["password"])
            # 刷新验证码
            browser.find_element_by_xpath(xpath_info["code_image_url"]).click()
            browser.find_element_by_xpath(xpath_info["code_image_url"]).click()
            sleep(1)
            # 输入账号和密码
            username.send_keys(self.user_name)
            sleep(1)
            password.send_keys(self.password)
            # 获取验证码输入框
            check_code = browser.find_element_by_xpath(xpath_info["check_code"])
            # 截屏
            file_name = f"../Image/{self.area}-{self.product}.png"
            browser.save_screenshot(file_name)
            print("截图完毕")
            # 裁剪图像
            cut_img(file_name, img_size)
            # 识别图像
            code = ocr(image_type, file_name)
            print("识别完毕")
            # 输入验证码
            check_code.send_keys(code)
            print(code)
            # 点击登录
            browser.find_element_by_xpath(xpath_info["login_button"]).click()
            sleep(4)

        while True:
            try:
                login()
                browser.find_element_by_xpath(xpath_info["success_ele"])

            except UnexpectedAlertPresentException:
                browser.switch_to_alert().accept()
                browser.get(self.login_url)
                sleep(1)
            except:
                browser.refresh()
            else:
                break

        # 获取cookie
        cookie = browser.get_cookies()
        browser.quit()
        print(cookie)
        return cookie

    def check_get_token(self, xpath_info, img_size, image_type, token_field):
        """
        xpath_info : 表单元素的xpath组成的字典
        xpath["username"] : 账号的xpath
        xpath["password"] : 密码的xpath
        xpath["check_code"] : 验证码输入框的xpath
        xpath["code_image_url"] : 验证码图片img的xpath
        xpath["login_button"] : 登陆按钮的xpath
        xpath["success_ele"] : 登陆成功后的任意一个页面元素的xpath
        """
        # 模拟浏览器
        browser = Chrome()
        browser.minimize_window()
        # 登录url
        login_url = self.login_url
        # 进入登录页面
        browser.get(login_url)

        def login():
            # 获取帐号+密码
            username = browser.find_element_by_xpath(xpath_info["username"])
            password = browser.find_element_by_xpath(xpath_info["password"])
            # 刷新验证码
            browser.find_element_by_xpath(xpath_info["code_image_url"]).click()
            browser.find_element_by_xpath(xpath_info["code_image_url"]).click()
            sleep(1)
            # 输入账号和密码
            username.send_keys(self.user_name)
            sleep(1)
            password.send_keys(self.password)
            # 获取验证码输入框
            check_code = browser.find_element_by_xpath(xpath_info["check_code"])
            # 截屏
            file_name = f"../Image/{self.area}-{self.product}.png"
            browser.save_screenshot(file_name)
            print("截图完毕")
            # 裁剪图像
            cut_img(file_name, img_size)
            # 识别图像
            code = ocr(image_type, file_name)
            print("识别完毕")
            # 输入验证码
            check_code.send_keys(code)
            print(code)
            # 点击登录
            browser.find_element_by_xpath(xpath_info["login_button"]).click()
            sleep(4)

        while True:
            try:
                login()
                browser.find_element_by_xpath(xpath_info["success_ele"])

            except UnexpectedAlertPresentException:
                browser.switch_to_alert().accept()
                browser.get(self.login_url)
                sleep(1)
            except:
                browser.refresh()
            else:
                break

        js = f"var token=window.localStorage.{token_field}; return token"
        token = browser.execute_script(js)
        browser.quit()
        print(token)
        return token

    # 将数据写入MySQL数据库
    def write_sql(self, ht_info):
        # 连接数据库
        connect = pymysql.connect("localhost", "root", "123456", "spider", 3306)
        # 获取游标
        cursor = connect.cursor()
        # 生成SQL语句
        info = {
            "产品名称": self.product,
            "地区": self.area,
            "注册人数": ht_info["注册人数"],
            "实名人数": ht_info["实名人数"],
            "申请人数": ht_info["申请人数"],
            "放款人数": ht_info["放款人数"],
            "当前时间": str(self.now),
            "备注": ht_info["备注"]
        }
        # sql = 'INSERT INTO ht_data value("{产品名称}","{地区}",{注册人数},{实名人数},{申请人数},{放款人数},"{当前时间}", 1)'.format_map(info)
        # 执行SQL语句
        sql = """
            insert into  ht_data (product_name,
            register_count,realname_count,apply_count,success_count,now,status,remark)
             VALUES ("{产品名称}",{注册人数},{实名人数},{申请人数},{放款人数},"{当前时间}", 1, "{备注}") 
            on DUPLICATE KEY UPDATE  product_name = VALUES(`product_name`),
            register_count = VALUES(`register_count`),
            apply_count = VALUES(`apply_count`),
            realname_count = VALUES(`realname_count`),
            success_count = VALUES(`success_count`),
            now = VALUES(`now`),
            status = VALUES(`status`), 
            remark = VALUES(`remark`)""".format_map(info)
        cursor.execute(sql)
        # 提交事务
        connect.commit()
        print(info)
        # 关闭连接
        cursor.close()
        connect.close()
