# -*- coding: utf-8 -*-
"""
@Time:   2020/12/31 10:21
@Author: Hudaiguo
@python version: 3.5.2
"""
import cv2
import numpy as np
from skimage import filters


def img_blur(img):
    """
    #图像模糊
    :param img:真彩图像
    :return:模糊后的图像
    """
    gaussian_blur_img = cv2.GaussianBlur(img, (9, 9), 0)
    median_blur_img = cv2.medianBlur(img, 9)

    return gaussian_blur_img, median_blur_img


def img_blur_detect(img_gray):
    """
    # 通过skimage调用sobel方法计算梯度，求图像的模糊程度
    :param img_gray: 输入灰度图像
    :return: 输出模糊程度得分,得分越低越模糊
    """
    tmp = filters.sobel(img_gray)  # 使用Sobel变换查找边缘量值,  输出：2维数组索贝尔(sobel)边缘映射。
    score = round(np.sqrt(np.sum(tmp ** 2)), 3)
    return score


def blur_detect(img_gray):
    """
    #通过矩阵复现sobel算法计算梯度，求图像的模糊程度
    :param img_gray:输入灰度图像
    :return:输出模糊程度得分,得分越低越模糊
    """
    kernel_x = np.array([[-1,-2,-1],
                         [0,0,0],
                         [1,2,1]])/4
    result_h = cv2.filter2D(img_gray/255,-1,kernel_x)
    result_h[:, 0] = 0.0
    result_h[:,-1] = 0.0
    kernel_y = np.array([[-1,0,1],
                       [-2,0,2],
                       [-1,0,1]])/4
    result_v = cv2.filter2D(img_gray/255,-1,kernel_y)
    result_v[0, :] = 0.0
    result_v[-1,:] = 0.0
    result = (result_h**2 + result_v**2)/2
    score = round(np.sqrt(np.sum(result)), 3)

    return score


if __name__ == "__main__":
    img_gray = cv2.imread("./err/test1.bmp", 0)
    s1 = img_blur_detect(img_gray)
    s2 = blur_detect(img_gray)
    print("模糊程度，s1={}, s2={}".format(s1, s2))
