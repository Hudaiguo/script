# -*- coding: utf-8 -*-
"""
@Time:   2020/12/17 16:56
@Author: Hudaiguo
@python version: 3.5.2
"""
# import configparser
import cv2
import numpy as np


def write_config(h0, w0, h1, w1, area_num, area, is_horizontal = "True", config_path = "config.ini"):
    """写配置文件"""
    with open(config_path, "w+") as wd:
        txt = "[Anchor_point_coordinates]\nh0 = {}\nw0 = {}\nh1 = {}\nw1 = {}\npoint_num = {}\nanchor_era_th = {}\nis_horizontal = {}\nshow_img_flag = False".format(h0,w0,h1,w1,area_num,area,is_horizontal)
        wd.write(txt)


def process(src, h0, w0, h1, w1):
    """
    查找切分图像的定位点坐标
    :param src:输入图像
    :param h0:需要切分的图像左上角y坐标
    :param w0:需要切分的图像左上角x坐标
    :param h1:需要切分的图像右下角y坐标
    :param w1:需要切分的图像右下角x坐标
    :return:查找到的图像定位点坐标
    """
    is_horizontal = "True"
    cut_img = src[h0:h1, w0:w1]
    cut_img_h, cut_img_w = cut_img.shape[:2]
    cut_gray_img = cv2.cvtColor(cut_img, cv2.COLOR_BGR2GRAY)
    th, cut_bin_img = cv2.threshold(cut_gray_img, 175, 255, cv2.THRESH_BINARY)
    image, contours, hierarchy = cv2.findContours(cut_bin_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    zb, area = [], []
    for num, c in enumerate(contours):
        if num > 0:
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            box = np.int0(box)
            draw_img = cv2.drawContours(cut_img, [box], 0, (0, 0, 255), 1)
            zb.append(box)
            area_ = abs((box[0][0]-box[3][0])*(box[0][1]-box[1][1]))
            area.append(area_)
    ave_area = int(sum(area) / len(area))
    print("定位点平均面积：", int(ave_area))
    print("定位点个数：", len(area))
    if cut_img_h < cut_img_w:
        print("定位点排列顺序：横排")
    else:
        print("定位点排列顺序：竖排")
        is_horizontal = "False"
    print("请确认定位点数量是否正确，不正确可以手动修改config.ini配置文件")
    print("############再按esc键退出############")
    cv2.imshow("draw_img", draw_img)
    cv2.waitKey(0)

    return ave_area, len(area), is_horizontal


def cut_img_local(event,x,y,flags,param):
    """获取需要切分图像的两顶点坐标"""
    global x1,y1
    if event == cv2.EVENT_LBUTTONDOWN:
        x1, y1 = x, y
        print("切分图像坐标(x1, y1):({},{})".format(x1, y1))
        cv2.circle(img, (x, y), 2, (0, 0, 255), -1)
    elif event == cv2.EVENT_RBUTTONDOWN:
        x2, y2 = x, y
        print("切分图像坐标(x2, y2):({},{})".format(x2, y2))
        cv2.circle(img, (x, y), 2, (0, 0, 255), -1)
        cv2.rectangle(img, (x1,y1), (x,y), (0, 255, 0), 1)
        cv2.imshow("img", img)
        area, area_num, is_horizontal = process(img, y1, x1, y2, x2)
        write_config(str(y1), str(x1), str(y2), str(x2), str(area_num), str(area), is_horizontal)


def cv2_imread(img_path, flag=1):
    """
    读取中文路径的图像。 flag<0:多通道； flag=0:灰度图； flag>0:真彩图。
    :param img_path:image path
    :param flag: flag<0:多通道； flag=0:灰度图； flag>0:真彩图.
    :return: image matrix
    """
    return cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), flag)


if __name__ == "__main__":
    img_path = input("输入图像路径：")
    img = cv2_imread(img_path)
    # print("############提示:先按鼠标左键选需要的定位点左上角，再按鼠标右键选需要的定位点右下角############")
    cv2.namedWindow('Press "esc" to exit')
    cv2.setMouseCallback('Press "esc" to exit', cut_img_local)
    while(True):
        cv2.imshow('Press "esc" to exit', img)
        if cv2.waitKey(20) & 0xFF== 27:
             break
