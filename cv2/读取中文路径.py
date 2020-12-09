# -*- coding: utf-8 -*-
"""
@Time:   2020/6/10 14:35
@Author: Hudaiguo
@python version: 3.5.2
"""
import cv2
import numpy as np


def im_read(img_path, flag=1):
    """
    读取中文路径的图像。 flag<0:多通道； flag=0:灰度图； flag>0:真彩图。
    :param img_path:image path
    :param flag: flag<0:多通道； flag=0:灰度图； flag>0:真彩图.
    :return: image matrix
    """
    return cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), flag)


if __name__ == "__main__":
    img_path = r""
    img = im_read(img_path, flag=0)
