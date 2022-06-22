#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/16 20:51
# @Author : 心蓝
from test_cases.base_case import BaseTest
from common.myddt import ddt, data
from common.test_data_handler import get_test_data_from_excel


cases = get_test_data_from_excel(BaseTest.settings.TEST_DATA_FILE, 'invest_flow')


@ddt
class TestInvestFlow(BaseTest):
    name = '投资业务流'

    @data(*cases)
    def test_invest_flow(self, case):
        self.checkout(case)