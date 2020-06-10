# -*- coding: utf-8 -*-
"""
@Time:   2020/6/10 14:13
@Author: Hudaiguo
@python version: 3.5.2
"""

import json


def read_json(read_path):
    """
    载入json数据。
    :param read_path: json文件的路径及名称。
    :return: 字典类型数据
    """
    with open(read_path, "r", encoding="utf-8") as json_fd:
        return json.load(json_fd)


def write_json(save_path):
    """
    将字典数据保存为json格式数据,一行一条数据且按keys排序。
    :param save_path: 保存json文件的路径及名称。
    :return: None
    """
    model = {}
    with open(save_path, 'a+', encoding='utf-8') as json_ad:
        json.dump(model, json_ad, ensure_ascii=False, indent=1, sort_keys=True)


if __name__ == "__main__":
    path = r""
    write_json(path)
    path = r"char_map.json"
    char_map = read_json(path)
