# -*- coding: utf-8 -*-
"""
@Time:   2020/12/31 17:05
@Author: Hudaiguo
@python version: 3.5.2
"""

import time
import grpc
import img_blur_detected_pb2 as pb2
import numpu as np
import cv2
import img_blur_detected_pb2_grpc as pb2_grpc

def data2img(img_data):
    return

class img_blur_detected(pb2_grpc.img_blur_detectedServicer):

    def blur_detect(self, request, context):
        """
        #通过矩阵复现sobel算法计算梯度，求图像的模糊程度
        :param img_gray:输入灰度图像
        :return:输出模糊程度得分,得分越低越模糊
        """
        img_gray = request.img_gray
        kernel_x = np.array([[-1, -2, -1],
                             [0, 0, 0],
                             [1, 2, 1]]) / 4
        result_h = cv2.filter2D(img_gray / 255, -1, kernel_x)
        result_h[:, 0] = 0.0
        result_h[:, -1] = 0.0
        kernel_y = np.array([[-1, 0, 1],
                             [-2, 0, 2],
                             [-1, 0, 1]]) / 4
        result_v = cv2.filter2D(img_gray / 255, -1, kernel_y)
        result_v[0, :] = 0.0
        result_v[-1, :] = 0.0
        result = (result_h ** 2 + result_v ** 2) / 2
        score = round(np.sqrt(np.sum(result)), 3)

        return score