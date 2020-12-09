# -*- coding: utf-8 -*-
"""
@Time:   2020/6/18 15:37
@Author: Hudaiguo
@python version: 3.5.2
"""

import configparser as cp


def parser_cfg_file(cfg_file):
    """
    #配置文件的读取
    :param cfg_file: 配置文件的路径
    :return: 配置文件内容
    """
    net_params = {}
    train_params = {}

    config = cp.ConfigParser()  # 实例
    config.read(cfg_file)

    for section in config.sections():
        # 获取配置文件中的net信息
        if section == 'net':
            for option in config.options(section):
                net_params[option] = config.get(section, option)

        # 获取配置文件中的train信息
        if section == 'train':
            for option in config.options(section):
                train_params[option] = config.get(section, option)

    return net_params, train_params


if __name__ == '__main__':
    net_params_, train_params_ = parser_cfg_file('../net.cfg')
    print(net_params_, "\n", train_params_)

    # 配置文件的添加和保存
    config = cp.ConfigParser()  # 类中一个方法 #实例化一个对象

    config["DEFAULT"] = {'ServerAliveInterval': '45',
                         'Compression': 'yes',
                         'CompressionLevel': '9',
                         'ForwardX11': 'yes'
                         }  # 类似于操作字典的形式

    config['bitbucket.org'] = {'User': 'Atlan'}  # 类似于操作字典的形式

    config['topsecret.server.com'] = {'Host Port': '50022', 'ForwardX11': 'no'}

    with open('example.ini', 'w') as configfile:
        config.write(configfile)  # 将对象写入文件
