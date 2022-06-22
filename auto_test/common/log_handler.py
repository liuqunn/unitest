#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/31 20:29
# @Author : 心蓝
"""
日志处理模块
"""
import logging


def get_logger(name, filename, mode='a', encoding='utf-8', fmt=None, debug=False):
    """

    :param name: 日志器的名字
    :param filename: 日志文件名
    :param mode: 文件模式
    :param encoding: 字符编码
    :param fmt: 日志格式
    :param debug: 调试模式
    :return:
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # 文件处理器的等级一般情况一定比控制要高
    if debug:
        file_level = logging.DEBUG
        console_level = logging.DEBUG
    else:
        file_level = logging.WARNING
        console_level = logging.INFO

    if fmt is None:
        fmt = '%(levelname)s %(asctime)s [%(filename)s-->line:%(lineno)d]:%(message)s'

    file_handler = logging.FileHandler(filename=filename, mode=mode, encoding=encoding)
    file_handler.setLevel(file_level)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)

    formatter = logging.Formatter(fmt=fmt)
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger


if __name__ == '__main__':
    logger = get_logger(name='py38', filename='../logs/py38.log', debug=True)
    logger.info('我是普通信息')

