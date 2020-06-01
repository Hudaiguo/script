# -*- coding:utf-8 -*-
"""
@Time:   2020/6/1 17:10
@Author: Hudaiguo
@python version: 3.5.2
"""

import cv2
import numpy as np

#从指定的内存缓存中读取数据，并把数据转换(解码)成图像格式;主要用于从网络传输数据中恢复出图像。
cv2.imdecode(buf=, flags=)
#将图片格式转换(编码)成流数据，赋值到内存缓存中;主要用于图像数据格式的压缩，方便网络传输。
cv2.imencode(ext=, img=, params=)


