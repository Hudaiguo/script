# -*- coding: utf-8 -*-
"""
@Time:   2021/1/4 10:01
@Author: Hudaiguo
@python version: 3.5.2
"""
import os
import grpc
import cv2
import numpy as np
import img_blur_detected_pb2 as pb2
import img_blur_detected_pb2_grpc as pb2_grpc


def run(img_data):
    with grpc.insecure_channel('192.168.*.*:50061') as channel:
        client = pb2_grpc.img_blur_detectedStub(channel)
        data = pb2.img_gray_request(img_gray=img_data)
        reply = client.blur_detect(data)
    print(reply)


def img2data(img_path):
    img = cv2.imread(img_path)
    a = cv2.imencode(os.path.split(img_path)[1], img)[1]
    img_data = np.array(a).tostring()

    return img_data


if __name__ == '__main__':
    img_path = r"./test.jpg"
    img_data = img2data(img_path)
    run(img_data)

