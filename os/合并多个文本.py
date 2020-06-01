# -*- coding:utf-8 -*-
"""
@Time:   2020/6/1 14:35
@Author: Hudaiguo
@python version: 3.5.2
"""
import os

def merge_txt(save_txt_path, path):
    """
    #将多个文本合并到一个新建的文本之中。
    :param save_txt_path: 新建文本保存路径
    :param path: 需要合并的文本路径
    :return: None
    """
    with open(save_txt_path, "a+") as wd:
        for i in os.listdir(path):
            txt_path = os.path.join(path, i)
            with open(txt_path, "r") as fd:
                txt = fd.read()
                wd.write(txt)

if __name__ == "__main__":
    text_path = r""
    save_text_path = r""
    merge_txt(save_text_path, text_path)