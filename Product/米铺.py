# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 21:56
# @Author  : 逗比i
# @Project : Backstage
# @File    : 抱金砖.py
# @Software: PyCharm
# @Describe:

from requests import Session
from BaseSpider import BaseSpider
from DealWithCookie import cookie_to_dict
import time



class BJZ(BaseSpider):
    def __init__(self, account):
        super(BJZ, self).__init__(account)

    def get_info(self):
        # 设置session
        session = Session()
        header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        from_data = {
            "start": f"{self.today} 00: 00:00",
            "end": f"{self.tomorrow} 00: 00:00",
            "page": "1",
            "token": "eyJpdiI6Ik1aSDJYNnh0enVoZDB0c0Iyb0xsbHc9PSIsInZhbHVlIjoiZmQrVTlqRXhRWG1GMkd1WWtFU2xSR0dGRTZcL1lRVStRRGNPdGNHSXdvbEhOOG44bGI5a0FYVmkrUEo3ekp5NFZOOHYzU1pnajVUU2l3ZVJkc25cL21qb1owWGNLUE9STlF3RzBEdzZuc2VrQ0g5NHFSQzhQalU3VFc2OEZoSEYyMiIsIm1hYyI6ImJjNzBmOTY2NThkNjMzMDM5YjYzMDY0MzNhZjdkYTM1Nzg1MmJmZmNlN2NiNWI1MDc5NTNmZjMzZGNhNDNmOTEifQ==",
            "v": "02782241539070254"
        }

        url = 'https://back.api.51woncai.com/api/thirdChannel/list'
        response = session.post(url, headers=header,data=from_data)
        ss = response.json()['data']['total']
        # 获取结果
        result = {
            "注册人数": ss,
            "实名人数": "null",
            "申请人数": "null",
            "放款人数": "null"
        }
        self.write_sql(result)


WD = {
    "login_url": "",
    "area": "外地",
    "product": "米铺",
    "username": "",
    "password": "",
    "channel": ""
}


all_local = [WD]

while True:
    for each in all_local:
        BJZ(each).get_info()
    time.sleep(1200)

