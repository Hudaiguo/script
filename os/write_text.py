# -*- coding:utf-8 -*-
"""
@Time:   2020/6/1 10:34
@Author: Hudaiguo
@python version: 3.5.2
"""

import os


def write_txt(path, text):
    """
    write text.
    :param path: need write text path
    :param text: write text
    :return: None
    """
    with open(path, "w") as wd:
        wd.write(text)

if __name__ == "__main__":
    path = r""
    text = "test"
    write_txt(path, text)