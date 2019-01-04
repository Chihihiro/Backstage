# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 21:56
# @Author  : 逗比i
# @Project : Backstage
# @File    : 抱金砖.py
# @Software: PyCharm
# @Describe:

from requests import Session
from scrapy import Selector
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict


class YQS(BaseSpider):
    def __init__(self, account):
        super(YQS, self).__init__(account)

    def get_info(self):
        xpath_info = {
            "username": '//*[@id="form"]/div[1]/div/input',
            "password": '//*[@id="form"]/div[2]/div/input',
            "login_button": '//*[@id="form"]/div[4]/div/a[1]',
            "check_code": '//*[@id="form"]/div[3]/div/input',
            "code_image_url": '//*[@id="verify_img"]',
            "success_ele": '//*[@id="推广产品"]/span'
        }
        # 设置session
        session = Session()
        # 获取cookie
        cookie = self.check_get_cookie(xpath_info, (984, 454, 1148, 503), "10400")
        # 给session设置cookie
        session.cookies.update(cookie_to_dict(cookie))
        # page的url
        page_url = f"http://s.51jinkong.cn/admin/channelmenu/index?shop_id=86&the_year_month={self.today.year}-{self.today.month}"
        # 设置头部
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.80 Safari/537.36",
        }
        # 访问url
        response = session.get(page_url, headers=headers)
        # 获取html
        html = response.text
        # 构造选择器
        selector = Selector(text=html)
        # 获取数据
        info = selector.xpath('/html/body/div[4]/div/article/table[2]/tbody/tr[1]')
        registers = info.xpath('./td[2]/text()').extract()[0].strip()
        apply = info.xpath('./td[3]/font/text()').extract()[0]
        success = info.xpath('.//td[7]/font/text()').extract()[0]
        # 最终结果
        result = {
            "注册人数": registers,
            "实名人数": "null",
            "申请人数": apply,
            "放款人数": success
        }
        self.write_sql(result)


SH = {
    "login_url": "http://s.51jinkong.cn/admin/Channeladmin/login",
    "area": "上海",
    "product": "摇钱树",
    "username": "changchanghua",
    "password": "111",
    "channel": ""
}


all_local = [SH]
for each_local in all_local:
    spider = YQS(each_local)
    spider.get_info()











