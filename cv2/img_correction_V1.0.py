# -*- coding: utf-8 -*-
"""
@Time:   2020/12/17 9:09
@Author: Hudaiguo
@python version: 3.5.2
"""

import cv2
import numpy as np
import os
import math
import configparser


def process(src, h0, w0, h1, w1):
    """
    查找定位点坐标
    :param src:输入图像
    :param h0:需要切分的图像左上角y坐标
    :param w0:需要切分的图像左上角x坐标
    :param h1:需要切分的图像右下角y坐标
    :param w1:需要切分的图像右下角x坐标
    :return:查找到的图像定位点坐标
    """
    cut_img = src[h0:h1, w0:w1]
    cut_gray_img = cv2.cvtColor(cut_img, cv2.COLOR_BGR2GRAY)
    th, cut_bin_img = cv2.threshold(cut_gray_img, 175, 255, cv2.THRESH_BINARY)
    image, contours, hierarchy = cv2.findContours(cut_bin_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    zb = []
    for c in contours:
        # rect[0]返回矩形的中心点; rect[1]返回矩形长和宽; rect[2]返回旋转角度,角度计算不如下面方法准确
        rect = cv2.minAreaRect(c)
        # 四个顶点坐标
        box = cv2.boxPoints(rect)
        box = np.int64(box)
        zb.append(box)
    zb = zb[1:]

    return cut_img, zb


def angle(cut_img, zb, point_num, anchor_era_th, img_file_path, is_horizontal="True", show_img_flag=False):
    """
    计算图像需要旋转的角度
    :param cut_img:切分之后的图像矩阵
    :param zb:检测定位点的坐标
    :param point_num:定位点数量
    :param anchor_era_th:定位点区域面积
    :param img_file_path:图像路径，用于写日志
    :param is_horizontal:定位点是否横排："True"横排，其他为竖排
    :param show_img_flag:是否显示查找到的定位点图像
    :return:计算旋转角度是否正常，需要旋转的角度。 True:处理正常
    """
    new_zb = []
    for i in zb:
        zb_mj = abs((i[0][0]-i[-1][0]) * (i[0][-1]-i[1][-1]))
        if anchor_era_th*0.8 < zb_mj < anchor_era_th*1.2:
            new_zb.append(i)
    if show_img_flag == "True":
        for c in new_zb:
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            draw_img = cv2.drawContours(cut_img, [box], 0, (0, 0, 255), 1)
        cv2.imshow('red img is found anchor point', draw_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    if 1 < len(new_zb) <= point_num:
        # w, h
        pt0 = new_zb[-1][0]
        pt1 = new_zb[0][0]
        y = pt1[-1] - pt0[-1]
        x = pt1[0] - pt0[0]
        if is_horizontal=="True":
            sita = (math.atan(y/x)/3.14159)*180
        else:
            sita = -(math.atan(x/y)/3.14159)*180
        return True, sita
    else:
        print("******************************************************")
        print("图像定位点数量错误，<2个或大于{}个定位点".format(point_num))
        print("******************************************************")
        write_log_txt("{}, err2:图像定位点数量{}个，<2个或大于{}个定位点，检查配置文件定位点数量。".format(img_file_path, len(new_zb), point_num))
        return False, 0


def rotate(img, sita):
    """
    #旋转输入图像
    :param img: 输入图像矩阵
    :param sita: 需要旋转的角度
    :return: 旋转之后的图像矩阵
    """
    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    m = cv2.getRotationMatrix2D(center, sita, 1.0)
    rotated = cv2.warpAffine(img, m, (w, h), borderValue=(255, 255, 255))

    return rotated


def read_ini(ini_path="config.ini"):
    # 读取ini配置文件
    cf = configparser.ConfigParser()
    cf.read(ini_path)
    h0, w0 = int(cf.get("Anchor_point_coordinates", "h0")), int(cf.get("Anchor_point_coordinates", "w0"))
    h1, w1 = int(cf.get("Anchor_point_coordinates", "h1")), int(cf.get("Anchor_point_coordinates", "w1"))
    point_num = int(cf.get("Anchor_point_coordinates", "point_num"))
    anchor_era_th = int(cf.get("Anchor_point_coordinates", "anchor_era_th"))
    is_horizontal = cf.get("Anchor_point_coordinates", "is_horizontal")
    show_img_flag = cf.get("Anchor_point_coordinates", "show_img_flag")

    return h0, w0, h1, w1, point_num, anchor_era_th, is_horizontal, show_img_flag


def write_log_txt(text, log_ini_path="log.txt"):
    with open(log_ini_path, "a+") as wd:
        wd.write(text + "\n")


def cv2_imread(img_path, flag=1):
    """
    读取含有中文路径的图像。 flag<0:多通道； flag=0:灰度图； flag>0:真彩图。
    :param img_path:image path
    :param flag: flag<0:多通道； flag=0:灰度图； flag>0:真彩图.
    :return: image matrix
    """
    return cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), flag)


def cv2_imwrite(img_path, img):
    """
    存储含有中文路径的图像。
    """
    cv2.imencode(os.path.splitext(img_path)[1], img)[1].tofile(img_path)


def main():
    img_path = os.path.abspath(input("输入需要旋转的图像文件夹："))
    if not os.path.exists(img_path):
        print("需要旋转的图像文件夹:  {},不存在！".format(img_path))
        return 0
    save_path = './processed_img'
    save_err_path = './err_img'
    h0, w0, h1, w1, point_num, anchor_era_th, is_horizontal, show_img_flag = read_ini("config.ini")
    num = 1
    for root, dirs, files in os.walk(img_path):
        for file in files:
            img_file_path = os.path.join(root, file)
            try:
                img_ori = cv2_imread(img_file_path)
                # img_ori1 = copy.copy(img_ori)
            except Exception:
                print("******************************************************")
                print("{}, 图像读取失败，检查是否含有非图像文件".format(file))
                print("******************************************************")
                write_log_txt("{}, Err1:图像读取失败，检查是否含有非图像文件。".format(img_file_path))
                continue
            cut_img, zb = process(img_ori, h0, w0, h1, w1)
            flag, sita = angle(cut_img, zb, point_num, anchor_era_th, img_file_path, is_horizontal=is_horizontal, show_img_flag=show_img_flag)
            new_img = rotate(img_ori, sita)
            if flag:
                save_path_new = os.path.join(save_path, root[(len(img_path)+1):])
            else:
                save_path_new = os.path.join(save_err_path, root[(len(img_path)+1):])
            if not os.path.exists(save_path_new):
                os.makedirs(save_path_new)
            if not cv2.imwrite(os.path.join(save_path_new, file), new_img):
                cv2_imwrite(os.path.join(save_path_new, file), new_img)
            print("{},已完成{}幅图像,旋转角度为：{}".format(file, num, round(sita,2)))
            num += 1


if __name__ == "__main__":
    main()
    print("\n************************已结束************************\n")
