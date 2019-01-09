# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月20日 10:56
# @Author  : 逗比i
# @Project : Real-Time-Data
# @File    : 贷款大师.py
# @Software: PyCharm
# @Describe: 



from time import sleep
from BaseSpider import BaseSpider
from scrapy import Selector
from selenium import webdriver

class Spider06(BaseSpider):

    def __init__(self, account):
        super(DRB, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="txtName"]',
            "password": '//*[@id="txtPwd"]',
            "login_button": '//*[@id="btnLogin"]',
            "check_code": '',
            "code_image_url": '',
            "success_ele": ''
        }

        login_url = "http://bb.jiedianqian.com/login"
        # 访问登录地址
        if self.area == "上海":
            # 输入token
            browser.find_element_by_id("token").send_keys("MgTYyGwqTvjDtyaP")
            # 查询
            browser.find_element_by_xpath('//*[@id="main"]/div[1]/div[2]/div/form/div[3]/input[1]').click()
            sleep(8)
        # 倒序排序
        browser.find_element_by_xpath('//*[@id="result"]/thead/tr/th[1]').click()
        sleep(1)
        # 构建Selector
        selector = Selector(text=browser.page_source)
        # 获取表格
        table = selector.xpath('//table[@id="result"]/tbody')
        tr_list = table.xpath('./tr')
        info = []
        for each_tr in tr_list:
            value = each_tr.xpath('./td/text()').extract()
            if value[0] == str(self.today) and value[2] == self.channel:
                info.extend(value)
        while len(info) < 8:
            info.append("0")

        # 获取结果
        result = {
            "注册人数": info[3],
            "实名人数": "null",
            "申请人数": info[-3],
            "放款人数": info[-2]
        }

        self.write_sql(result)


SH = {
    "login_url": "http://bb.jiedianqian.com/login",
    "area": "上海",
    "product": "贷款大师",
    "username": "dkds_qzj690",
    "password": "caperu7@3n",
    "channel": "dkdsyqmcpa23"
}




















