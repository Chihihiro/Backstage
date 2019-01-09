# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月27日 20:28
# @Author  : 逗比i
# @Project : Backstage
# @File    : 超薪白卡.py
# @Software: PyCharm
# @Describe: 

import re
import requests
from scrapy import Selector
from BaseSpider import BaseSpider
from tool.DealWithCookie import cookie_to_dict


class CXBK(BaseSpider):
    def __init__(self, account):
        super(CXBK, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="username"]',
            "password": '//*[@id="password"]',
            "login_button": '//*[@id="containerDiv"]/div[2]/form/div/button'
        }
        # 获取cookie
        cookie = self.no_check_get_cookie(xpath_info)
        # json的url
        json_url = f"http://aaa.miaosu1.xyz/index.php?g=Admin&m=User&a=index"
        # 设置session
        session = requests.session()
        session.cookies.update(cookie_to_dict(cookie))
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        args = {
            "stratdate": str(self.today),
            "enddate": str(self.today)
        }
        # 访问url
        response = session.get(json_url, headers=headers)
        # 构建Selector
        selector = Selector(text=response.text)
        # 获取注册数量
        register_user = selector.xpath('//*[@id="index"]/div[4]/text()').extract()[0]
        # print(register_user)
        # 获取结果
        result = {
            "注册人数": re.findall(r"共(\d+)条记录", register_user),
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null"
        }
        self.write_sql(result)


WD = {
    "login_url": "http://aaa.miaosu1.xyz/index.php?g=Admin&m=Index&a=index.php&g=Home&m=Index&a=index",
    "area": "外地",
    "product": "贷款大师",
    "username": "zhangzong01",
    "password": "123456",
    "channel": ""
}

all_local = [WD]
for each_local in all_local:
    spider = CXBK(each_local)
    spider.get_info()














