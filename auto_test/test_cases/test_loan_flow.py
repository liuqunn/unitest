#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/14 21:10
# @Author : 心蓝
from test_cases.base_case import BaseTest


class TestLoanFlow(BaseTest):
    name = '贷款业务流'

    def test_01register_normal_loan_user(self):
        """注册普通融资用户"""
        # 1. 测试数据
        case = {
            'title': '普通投资用户注册',
            'url': 'register',
            'method': 'post',
            'request': '{"headers": {"X-Lemonban-Media-Type": "lemonban.v1"},'
                       '"json":{"mobile_phone": #phone#, "pwd":"12345678"}}',
            'status_code': 200,
            'expect_data': '{"code":0, "msg": "OK"}',
        }
        # 2. 测试
        self.checkout(case)
        # 3. 传递依赖数据
        # 如果测试成功了，需要将注册好的电话号码，共享给下一个用例，绑定到类属性上
        self.__class__.mobile_phone = self.response.json()['data']['mobile_phone']

    def test_02login_normal_loan_user(self):
        """登陆普通融资用户"""
        # 1. 测试数据
        case = {
            'title': '普通融资用户登录',
            'url': 'login',
            'method': 'post',
            'request': '{"headers": {"X-Lemonban-Media-Type": "lemonban.v2"},'
                       '"json":{"mobile_phone":#mobile_phone#,"pwd":"12345678"}}',
            'status_code': 200,
            'expect_data': '{"code":0, "msg": "OK"}'
        }
        # 2. 测试
        self.checkout(case)
        # 3. 传递依赖数据
        self.__class__.normal_member_id = self.response.json()['data']['id']
        self.__class__.normal_token = self.response.json()['data']['token_info']['token']

    def test_03add_loan(self):
        """创建项目"""
        # 1. 测试数据
        case = {
            'title': '添加项目',
            'url': 'add',
            'method': 'post',
            'request': '''
                        {
                        "headers": {"X-Lemonban-Media-Type": "lemonban.v2","Authorization":"Bearer #normal_token#"},
                        "json":{
                        "member_id":#normal_member_id#,
                        "title":"实现财富自由",
                        "amount":5000,
                        "loan_rate":18.0,
                        "loan_term":6,
                        "loan_date_type":1,
                        "bidding_days":10}
                        }
                        ''',
            'status_code': 200,
            'expect_data': '{"code":0,"msg":"OK"}'
        }
        # 2. 测试
        self.checkout(case)
        # 3. 传递依赖数据
        self.__class__.loan_id = self.response.json()['data']['id']

    def test_04register_admin_user(self):
        """注册管理员用户"""
        # 1. 测试数据
        case = {
            'title': '注册管理员用户',
            'url': 'register',
            'method': 'post',
            'request': '{"headers": {"X-Lemonban-Media-Type": "lemonban.v1"},'
                       '"json": {"mobile_phone":#phone#,"pwd":"12345678","type":0}}',
            'status_code': 200,
            'expect_data': '{"code":0,"msg":"OK"}',
            'sql': 'SELECT id from member where mobile_phone = #phone#'
        }
        # 2. 测试
        self.checkout(case)
        # 3. 传递依赖数据
        self.__class__.admin_mobile_phone = self.response.json()['data']['mobile_phone']

    def test_05login_admin_user(self):
        """登录管理员用户"""
        # 1. 测试数据
        case = {
            'title': '管理员用户登录',
            'url': 'login',
            'method': 'post',
            'request': '{"headers": {"X-Lemonban-Media-Type": "lemonban.v2"},'
                       '"json": {"mobile_phone":#admin_mobile_phone#,"pwd":"12345678"}}',
            'status_code': 200,
            'expect_data': '{"code":0,"msg":"OK"}',
        }
        # 2. 测试
        self.checkout(case)
        # 3. 传递依赖数据
        self.__class__.admin_token = self.response.json()['data']['token_info']['token']

    def test_06audit_loan(self):
        """审核项目"""
        # 1. 测试数据
        case = {
            'title': '审核项目',
            'url': 'audit',
            'method': 'patch',
            'request': '''
                        {
                        "headers": {"X-Lemonban-Media-Type": "lemonban.v2","Authorization":"Bearer #admin_token#"},
                        "json":{"loan_id":#loan_id#,"approved_or_not":true}
                        }
                        ''',
            'status_code': 200,
            'expect_data': '{"code":0,"msg":"OK"}'

        }
        # 2. 测试
        self.checkout(case)
