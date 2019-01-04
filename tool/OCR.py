# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 20:45
# @Author  : 逗比i
# @Project : Backstage
# @File    : OCR.py
# @Software: PyCharm
# @Describe: 
from fateadm_api import TestFunc


def ocr(api_type, file_name):
    # 识别验证码
    code = TestFunc(api_type, file_name)
    return code

















