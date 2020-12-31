# -*- coding: utf-8 -*-
"""
@Time:   2020/12/22 14:48
@Author: Hudaiguo
@python version: 3.5.2
"""

#学习图像流数据
#cv2.imdecode()函数从指定的内存缓存中读取数据，并把数据转换(解码)成图像格式;主要用于从网络传输数据中恢复出图像。
#cv2.imencode()函数是将图片格式转换(编码)成流数据，赋值到内存缓存中;主要用于图像数据格式的压缩，方便网络传输。

#将图片编码到缓存，并保存到本地：
import numpy as np
import cv2
from io import BytesIO
from PIL import Image
#转为流数据，服务使用
img = cv2.imread(r'D:\desktop\20410102110007.jpg')
a = cv2.imencode('.jpg', img)[1]  #编码为一维图像流
print("图像流:", a)
b = np.array(a).tostring()
print("图像流:", b)

#图像流转jpg
img = cv2.imdecode(np.frombuffer(b, np.uint8), cv2.IMREAD_COLOR)
cv2.imshow("img", img)
cv2.waitKey(0)
input()
#存储含有中文路径的图像
img_path = r'D:\desktop\2.jpg'
img = cv2.imread(img_path)
a1 = cv2.imencode(".jpg", img)[1]  #编码为一维图像流
a2 = a1.tofile(img_path)


#读取含有中文路径的图像
c = np.fromfile(img_path, dtype=np.uint8)
print("c:", c)
img = cv2.imdecode(c, 1) #解码为图像矩阵
input()

#下行代码：imgs为图像列表

# 缓存数据保存到本地
# with open('img_encode.txt', 'wb') as f:
#     f.write(str_encode)
#     f.flush
