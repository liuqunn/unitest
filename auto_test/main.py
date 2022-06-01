#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/26 20:08
# @Author : 心蓝
import unittest

import pytest

import settings
from common.report_handler import report

if __name__ == '__main__':
    # 收集用例并返回测试套件
    # ts = unittest.TestLoader().discover('test_cases')
    # report(ts, **settings.REPORT_CONFIG)
    pytest.main(['-v', '--alluredir=reports', 'test_cases']) .