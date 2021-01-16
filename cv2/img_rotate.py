# -*- coding: utf-8 -*-
"""
@Time: 2021/1/14 12:38 
@Author: Hudaiguo
@python version: 3.5.2
"""

import os
import cv2
import numpy as np

def cv2_imread(img_path, flag=1):
    return cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), flag)


def cv2_imwrite(img_path, img):
    cv2.imencode(os.path.splitext(img_path)[1], img)[1].tofile(img_path)

if __name__ == "__main__":
    img_path = input("input img path: ")
    rotate = int(input("shunshizhen 90*n. n=:"))
    num = 1
    for root, dirs, files in os.walk(img_path):
        for file in files:
            img_file_path = os.path.join(root, file)
            #save_file_path = img_file_path.replace("94", "94_")
            try:
                img = cv2_imread(img_file_path)
                
                for i in range(rotate%4):
                    img = cv2.transpose(img)
                    img = cv2.flip(img, 1)
                new_img = img
            except Exception:
                with open("err.txt", "a+")as f:
                    f.write("err1:    {} \n".format(img_file_path))
                continue
            #if not os.path.exists(os.path.dirname(save_file_path)):
            #    os.makedirs(os.path.dirname(save_file_path))
            cv2_imwrite(img_file_path, new_img)
            print("have processed：{}".format(num))
            num += 1
    print("end")
    input()
