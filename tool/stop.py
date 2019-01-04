#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/12/28 0028 14:03 
# @Author : Chihiro 
# @Site :  
# @File : stop.py 
# @Software: PyCharm

import pymysql
from time import sleep

def update():
    connect = pymysql.connect('192.168.10.180','root1','123456','spider',3306)

    cursor = connect.cursor()
    area = input("请输入地区：    ")
    sql = 'update ht_data set `status` = 0 where product_name = "{product_name}" and area = "{area}";'.format_map({
        "product_name": input("请输入产品名称：    "),
        "area": area if area.strip() != "安徽" else "外地",
    })

    try:
        cursor.execute(sql)
    except:
        connect.rollback()
        print("修改失败!!!!")
    else:
        connect.commit()
        print("修改成功")

    cursor.close()
    connect.close()
    print("10s后关闭窗口")
    sleep(10)


update()


