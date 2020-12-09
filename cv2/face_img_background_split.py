# -*- coding: utf-8 -*-
"""
@Time:   2020/12/02 14:45
@Author: Hudaiguo
@python version: 3.5.2
"""

import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

def face_detect_ROI(img_path):

        # 创建一个级联分类器 加载一个 .xml 分类器文件. 它既可以是Haar特征也可以是LBP特征的分类器.
        face_cascade = cv2.CascadeClassifier("../data/haarcascade_frontalface_default.xml") #人脸
        eye_cascade = cv2.CascadeClassifier("../data/haarcascade_eye_tree_eyeglasses.xml") #可检测带眼镜的
        eye_cascade2 = cv2.CascadeClassifier("../data/haarcascade_lefteye_2splits.xml") #睁开或闭着的眼睛
        eye_cascade1 = cv2.CascadeClassifier("../data/haarcascade_eye.xml") #仅睁开的眼睛
        upper_body = cv2.CascadeClassifier("../data/haarcascade_upperbody.xml") #上半身
        # 加载图像
        img = cv2.imread(img_path)
        # 转换为灰度图
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 进行人脸检测，传入scaleFactor，minNegihbors，分别表示人脸检测过程中每次迭代时图像的压缩率以及
        # 每个人脸矩形保留近似数目的最小值
        # 返回人脸矩形数组
        faces = face_cascade.detectMultiScale(gray_img, 1.3, 5)
        for (x, y, w, h) in faces:
            # 在原图像上绘制矩形
            img = cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

            roi_gray = gray_img[y:y + h, x:x + w]
            # 眼睛检测
            eyes = eye_cascade.detectMultiScale(roi_gray, 1.03, 5, 0, (40, 40))
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(img, (ex + x, ey + y), (x + ex + ew, y + ey + eh), (0, 255, 0), 2)


        cv2.namedWindow('Face Detected！')
        cv2.imshow('Face Detected！', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


def face_detect_ROI_1(img_path):

    face_cascade = cv2.CascadeClassifier("../data/haarcascade_frontalface_default.xml")  # 人脸
    # 加载图像
    img = cv2.imread(img_path)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 返回人脸矩形数组 #[x,y,w,h]
    faces_local = face_cascade.detectMultiScale(gray_img, 1.3, 5)
    face_img = []
    for (x, y, w, h) in faces_local:
        face_img.append(img[y:y+h, x:x+w])

    return  faces_local, face_img



def split_background(img_path, r=(0,0,0,0)):
    #Grabcut算法
    #去除模版里的孔洞
    #初步增加感兴趣区域，不需要人手动
    #如果要避免毛刺 可以显示矩形框，显示人头像  轮廓近似   #cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    src = cv2.imread(img_path)
    h, w = src.shape[:2]
    r = (1, 1, w, h)
    # r = cv2.selectROI('input', src, False, False)  # 返回 (x_min, y_min, w, h)
    # print(r)
    # roi区域
    # roi = src[int(r[1]):int(r[1] + r[3]), int(r[0]):int(r[0] + r[2])]
    # img = src.copy()
    # cv2.rectangle(img, (int(r[0]), int(r[1])), (int(r[0]) + int(r[2]), int(r[1]) + int(r[3])), (255, 0, 0), 2)

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
    cv2.imwrite("result_"+os.path.split(img_path)[1], result)


def split_background_1(img_path, r=(0,0,0,0)):
    #Grabcut算法
    #去除模版里的孔洞
    #初步增加感兴趣区域，不需要人手动
    #如果要避免毛刺 可以显示矩形框，显示人头像  轮廓近似  #cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    src = cv2.imread(img_path)
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

def detect_img_light(img):

    if len(img) == 1:
        img_gray = cv2.cvtColor(img[0], cv2.COLOR_BGR2GRAY)
        # hist = cv2.calcHist([img],[0],None,[256],[0,255])
        plt.subplot(121)
        plt.imshow(img_gray, cmap='gray')
        plt.subplot(122)
        plt.hist(img_gray.ravel(), 256, [0, 256])
        plt.show()
        # imgs = np.hstack([img_gray, hist])

    elif len(img) > 1:
        for img_ in img:
            img_gray = cv2.cvtColor(img_, cv2.COLOR_BGR2GRAY)
            #hist = cv2.calcHist([img],[0],None,[256],[0,255])
            #plt.subplot(131)
            # plt.imshow(img, cmap='gray') #彩图
            plt.subplot(121)
            plt.imshow(img_gray, cmap='gray')
            plt.subplot(122)
            plt.hist(img_gray.ravel(), 256, [0, 256])
            plt.show()
    else:
        print("未检测到人脸！")

if __name__ == '__main__':
    img_root = r"../10_face_detect/face_img_test"
    for img_name in os.listdir(img_root):
        img_path = os.path.join(img_root, img_name)
        print(img_path)
        # img = cv2.imread(img_path)
        # face_detect_ROI(img_path)
        # split_background(img_path)
        faces_local, face_img = face_detect_ROI_1(img_path)
        detect_img_light(face_img)

