# !/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time    : 2018年12月26日 23:25
# @Author  : 逗比i
# @Project : Backstage
# @File    : cut_img.py
# @Software: PyCharm
# @Describe: 

from PIL import Image


def cut_img(filename, size):
    # 打开图片
    old_image = Image.open(filename)
    # 转为灰度图像
    old_image = old_image.convert("L")
    # img2 = img.crop((300, 376, 600, 405))
    # 裁剪图片
    new_image = old_image.crop(size)
    # 保存图片
    new_image.save(filename)


# cut_img("3.png", (982, 450, 1145, 503))
