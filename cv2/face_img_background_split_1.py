# -*- coding: utf-8 -*-
"""
@Time:   2020/12/02 14:45
@Author: Hudaiguo
@python version: 3.5.2
"""

import os
import cv2
import numpy as np


def split_background_1(src, r=(1,1,100,100)):
    """
    #前后景分离。Grabcut算法。
    :param img: 输入需要切分的图像矩阵
    :param r: 图像前后景缩小范围矩阵，这里应该需要人脸坐标提示，减少前后景背景分离的错误率
    :return:
    """
    h, w = src.shape[:2]
    r = (1, 1, w, h)
    # 原图mask
    mask = np.zeros(src.shape[:2], dtype=np.uint8)
    # 矩形roi
    rect = (int(r[0]), int(r[1]), int(r[2]), int(r[3]))  # 包括前景的矩形，格式为(x,y,w,h)
    bgdmodel = np.zeros((1, 65), np.float64)  # bg模型的临时数组  13 * iterCount
    fgdmodel = np.zeros((1, 65), np.float64)  # fg模型的临时数组  13 * iterCount
    cv2.grabCut(src, mask, rect, bgdmodel, fgdmodel, 11, mode=cv2.GC_INIT_WITH_RECT)
    # 提取前景和可能的前景区域
    mask2 = np.where((mask == 1) + (mask == 3), 255, 0).astype('uint8')
    B, G, R = cv2.split(src)
    B_ROI = cv2.bitwise_and(mask2, B)
    G_ROI = cv2.bitwise_and(mask2, G)
    R_ROI = cv2.bitwise_and(mask2, R)
    result = cv2.merge([B_ROI, G_ROI, R_ROI])

    return result


def face_cut(face_profile_list, face_img):
    """
    #通过人脸位置坐标获得人脸图像，将脸部区域根据坐标切割出来
    :param face_profile_list: 人脸轮廓坐标列表
    :param face_img: 人脸输入整体图像
    :return: 切割之后的人脸图像
    """
    pts = np.array(face_profile_list, np.int32)
    mask = np.zeros(face_img.shape, np.uint8)
    mask = cv2.polylines(mask, [pts], True, (255, 255, 255)) #pts必须为3维
    mask2 = cv2.fillPoly(mask, [pts], (255, 255, 255))      #填充多边形
    ROI = cv2.bitwise_and(mask2, face_img)
    #投影找出脸部区域、去除黑色背景
    gray_img = cv2.cvtColor(ROI, cv2.COLOR_BGR2GRAY)
    th, binary = cv2.threshold(gray_img, 100, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    img_bin_array = np.array(binary) / 255
    h, w = ROI.shape[:2]
    column_sum = img_bin_array.sum(axis=0)  # 列聚合
    rows_sum = img_bin_array.sum(axis=1)  # 行聚合
    for index_, num in enumerate(column_sum):
        if num > 0:
            img_L = index_
            break
    for index_, num in enumerate(column_sum[::-1]):
        if num > 0:
            img_R = w - index_
            break
    for index_, num in enumerate(rows_sum):
        if num > 0:
            img_U = index_
            break
    for index_, num in enumerate(rows_sum[::-1]):
        if num > 0:
            img_D = h - index_
            break
    ROI = ROI[img_U:img_D, img_L:img_R]

    return ROI


def non_zero_mean(np_arr):
    """
    #求矩阵非零像素平均值
    :param np_arr: 输入二维矩阵
    :return: 输出矩阵非零像素的平均值
    """
    exist = (np_arr != 0)
    num = np_arr.sum()
    den = exist.sum()

    return num/den


def uneven_light_detect_new2(face_img_list, Polarized_light_source_Th = 55):
    """
    #直接将输入人脸平均分四块，不进行提取皮肤
    #检测输入的人脸图像是否光线不均匀
    :param face_img_list:人脸图像列表，为空无返回值
    :param Polarized_light_source_Th = 55:偏光源阈值为55
    :return:光线是否不均匀判断数组，例如[True, False] True:光线不均匀 False:光线均匀
    :return:最大光线相差值
    """
    if len(face_img_list) >= 1:
        is_polarized_light_source = []
        for face_img in face_img_list:
            hsv_v = cv2.cvtColor(face_img, cv2.COLOR_BGR2HSV)[:, :, 2]
            h, w = hsv_v.shape
            hsv_v_11, hsv_v_12, hsv_v_21, hsv_v_22 = hsv_v[:int(h / 2), :int(w / 2)], \
                                                     hsv_v[:int(h / 2),int(w / 2):], \
                                                     hsv_v[int(h / 2):,:int(w / 2)], \
                                                     hsv_v[int(h / 2):,int(w / 2):]
            hsv_v_11_mean, hsv_v_12_mean, hsv_v_21_mean, hsv_v_22_mean = non_zero_mean(hsv_v_11),\
                                                                         non_zero_mean(hsv_v_12),\
                                                                         non_zero_mean(hsv_v_21),\
                                                                         non_zero_mean(hsv_v_22)
            max_line_diff = round(max(abs(hsv_v_11_mean - hsv_v_12_mean),\
                                    abs(hsv_v_21_mean - hsv_v_22_mean),\
                                    abs(hsv_v_11_mean - hsv_v_12_mean),\
                                    abs(hsv_v_12_mean - hsv_v_22_mean)), 2)
            if max_line_diff > Polarized_light_source_Th:
                # print("偏光源")
                is_polarized_light_source.append(True)
            else:
                # print("非偏光源")
                is_polarized_light_source.append(False)
        return is_polarized_light_source, max_line_diff
    else:
        return [False], 0

if __name__ == '__main__':
    img_root = r"face_img_test"
    Polarized_light_source_Th = 55
    for img_name in os.listdir(img_root):
        img_path = os.path.join(img_root, img_name)
        img = cv2.imread(img_path)
        split_bak_img = split_background_1(img)  #前后景分离
        #这里获取人脸轮廓检测算法省略
        landmark_shape = predictor(img, face_rectangle)
        landmarks = np.matrix([[p.x, p.y] for p in landmark_shape.parts()])  # 人脸坐标列表
        face_profile = np.vstack((np.array(landmarks[:17]), np.array(landmarks[17:27][::-1]))) #人脸轮廓坐标
        face_cut_img = face_cut(face_profile, img)
        w_, h_ = face_cut_img.shape[:2]
        w_new, h_new = 150, int(150 * (h_ / w_))
        face_cut_img_ = cv2.resize(face_cut_img, (w_new, h_new), interpolation=cv2.INTER_CUBIC)
        light_result, ave_light_diff = uneven_light_detect_new2(face_cut_img_, Polarized_light_source_Th = Polarized_light_source_Th)


