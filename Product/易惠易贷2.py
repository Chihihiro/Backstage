# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月27日 20:28
# @Author  : 逗比i
# @Project : Backstage
# @File    : 超薪白卡.py
# @Software: PyCharm
# @Describe: 

import requests
from scrapy import Selector
from BaseSpider import BaseSpider
from tool.DealWithCookie import cookie_to_dict


class CXBK(BaseSpider):
    def __init__(self, account):
        super(CXBK, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="pd-form-username"]',
            "password": '//*[@id="pd-form-password"]',
            "login_button": '//*[@id="login-form"]/div[5]/button'
        }
        # 获取cookie
        cookie = self.no_check_get_cookie(xpath_info)
        # json的url
        json_url = f"https://www.gglcqm.cn/admin/channel/counts/ids/153?addtabs=1"
        # 设置session
        session = requests.session()
        session.cookies.update(cookie_to_dict(cookie))
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 访问url
        response = session.get(json_url, headers=headers)
        # 构建Selector
        selector = Selector(text=response.text)
        # 获取注册数量
        register_user = selector.xpath('//*[@id="one"]/table/tbody/tr[1]/td/text()').extract()[2]
        # 获取结果
        result = {
            "注册人数": register_user,
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null"
        }
        self.write_sql(result)


WD = {
    "login_url": "https://www.gglcqm.cn/admin/index/login.html",
    "area": "外地",
    "product": "易惠易贷",
    "username": "15923176826",
    "password": "123456",
    "channel": ""
}

all_local = [WD]
for each_local in all_local:
    spider = CXBK(each_local)
    spider.get_info()














