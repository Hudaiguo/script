# -*- coding: utf-8 -*-
"""
@Time:   2020/12/31 17:05
@Author: Hudaiguo
@python version: 3.5.2
"""

import time
import grpc
import numpy as np
import cv2
import img_blur_detected_pb2_grpc as pb2_grpc
import img_blur_detected_pb2 as pb2
from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class img_blur_detected(pb2_grpc.img_blur_detectedServicer):

    def blur_detect(self, request, context):
        """
        #通过矩阵复现sobel算法计算梯度，求图像的模糊程度
        :param img_gray:输入灰度图像
        :return:输出模糊程度得分,得分越低越模糊
        """
        img_gray_data = request.img_gray
        img = cv2.imdecode(np.frombuffer(img_gray_data, np.uint8), cv2.IMREAD_COLOR)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # cv2.imshow("img_gray", img_gray)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
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
        score = str(round(np.sqrt(np.sum(result)), 3))
        print("服务端得分：", score)

        return pb2.score_reply(score=score)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    pb2_grpc.add_img_blur_detectedServicer_to_server(img_blur_detected(), server)
    server.add_insecure_port('[::]:50061')
    print("server will start at 127.0.0.1:50061")
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
