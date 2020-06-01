# -*- coding:utf-8 -*-
"""
@Time:   2020/6/1 16:53
@Author: Hudaiguo
@python version: 3.5.2
"""

import cv2
import numpy as np

def check_ocr(img, t0=70000, t1 = 130000):
    """
    #原理：通过腐蚀及外接矩形找出条形码的顶点坐标，然后通过坐标建立一个mask,与原图像求或
    input:三通道图像；条形码面积阈值，大于该值则返回标志0，否则返回1
    return:(标志位，0为不可信，1为可信；条形码被白色图像遮挡后的三通道原始图像）
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, img_bin = cv2.threshold(img_gray, 40, 255, cv2.THRESH_BINARY)
    kernel = np.ones((2, 3), np.uint8)
    img_fs = cv2.erode(img_bin, kernel, iterations=11)
    img_, contours, hierarchy = cv2.findContours(img_fs, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cons_area = sorted(contours, key=cv2.contourArea, reverse=True)[1]  # 根据区域面积进行排序
    img_area = cv2.contourArea(cons_area)
    # print(img_area)
    if img_area < t0 or img_area > t1:
        return (0, img)
    img_min_rec = cv2.minAreaRect(cons_area) #得到最小外接矩形的（中心(x,y), (宽,高), 旋转角度）
    box = cv2.boxPoints(img_min_rec) #得到顶点坐标
    pts = np.array([[int(i[0]), int(i[1])] for i in box])
    mask = np.zeros(img.shape, np.uint8)
    mask2 = cv2.fillPoly(mask, [pts], (255, 255, 255))
    ROI = cv2.bitwise_or(mask2, img)

    return (1, ROI)

if __name__ == "__main__":
    img_path = r""
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), -1)
    flag, img = check_ocr(img)