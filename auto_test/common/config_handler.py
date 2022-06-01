#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/2 20:14
# @Author : 心蓝
from configparser import ConfigParser

import yaml


def get_config(filename, encoding='utf-8') -> dict:
    """
    获取配置文件
    :param filename:
    :param encoding:
    :return:
    """
    # 1. 获取文件后缀名
    suffix = filename.split('.')[-1]
    # 2. 判断这个配置文件的类型
    if suffix in ['ini', 'cfg', 'cnf']:
        # ini配置
        conf = ConfigParser()
        conf.read(filename, encoding=encoding)
        # 讲ini配置信息解析成一个大字典
        data = {}
        for section in conf.sections():
            data[section] = dict(conf.items(section))

    elif suffix in ['yml', 'yaml']:
        # yaml配置
        with open(filename, 'r', encoding=encoding) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
    else:
        raise ValueError('不能识别的配置文件后缀')

    return data


class Config:
    def __init__(self, filename, encoding='utf-8'):
        # 初始化工作
        self.filename = filename
        self.encoding = encoding
        self.suffix = filename.split('.')[-1]
        if self.suffix not in ['ini', 'conf', 'cnf', 'yml', 'yaml']:
            raise ValueError('不能识别的配置文件后缀')

    def __parse_ini(self):
        """
        解析ini文件
        :return:
        """
        con = ConfigParser()
        con.read(self.filename, self.encoding)
        data = {}
        for section in con.sections():
            data[section] = dict(con.items(section))
        return data

    def __parse_yaml(self):
        """
        解析yaml文件
        :return:
        """
        with open(self.filename, 'r', encoding=self.encoding) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data

    def parse(self):
        """
        解析
        :return:
        """
        if self.suffix in ['yaml', 'yml']:
            return self.__parse_yaml()
        else:
            return self.__parse_ini()


if __name__ == '__main__':
    res = get_config('../config.yaml')
    print(res)
    res = get_config('../config.ini')
    print(res)

    config = Config('../config.ini')
    data = config.parse()
    print(data)