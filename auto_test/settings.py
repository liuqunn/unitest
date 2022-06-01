#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/2 20:48
# @Author : 心蓝
import os
# 项目路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 项目域名
PROJECT_HOST = 'http://api.lemonban.com/futureloan'
# 接口地址
INTERFACES = {
    'register': '/member/register',
    'login': '/member/login',
    'recharge': '/member/recharge',
    'add': '/loan/add',
    'audit': '/loan/audit',
    'invest': '/member/invest'
}

# 日志配置
LOG_CONFIG = {
    'name': 'py38',
    'filename': os.path.join(BASE_DIR, 'logs/py38.log'),
    'mode': 'a',
    'encoding': 'utf-8',
    'debug': True
}

# 测试数据配置
TEST_DATA_FILE = os.path.join(BASE_DIR, 'test_data/testcases.xlsx')

# 测试报告
REPORT_CONFIG = {
    'description': '前程贷',
    'filename': 'py38期测试报告.html',
    'report_dir': os.path.join(BASE_DIR, 'reports'),
    'title': 'py38期',
    'theme': 'theme_cyan',
    '_type': 'h'
}

# 数据库配置
DB_CONFIG = {
    'host': 'api.lemonban.com',
    'user': 'future',
    'password': '123456',
    'db': 'futureloan',
    'charset': 'utf8',
    'port': 3306,
    'autocommit': True  # 自动提交事务 防止可重复读的问题
}

# 服务器公钥
SERVER_RSA_PUB_KEY = """
-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDQENQujkLfZfc5Tu9Z1LprzedE
O3F7gs+7bzrgPsMl29LX8UoPYvIG8C604CprBQ4FkfnJpnhWu2lvUB0WZyLq6sBr
tuPorOc42+gLnFfyhJAwdZB6SqWfDg7bW+jNe5Ki1DtU7z8uF6Gx+blEMGo8Dg+S
kKlZFc8Br7SHtbL2tQIDAQAB
-----END PUBLIC KEY-----
"""