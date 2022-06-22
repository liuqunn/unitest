#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/9 21:27
# @Author : 心蓝
from test_cases.base_case import BaseTest
from common.myddt import ddt, data
from common.fixture import register, login, add_loan
from common.test_data_handler import (
    generate_no_use_phone,
    get_test_data_from_excel,
)


cases = get_test_data_from_excel(BaseTest.settings.TEST_DATA_FILE, 'audit')


@ddt
class TestAudit(BaseTest):
    name = '审核'

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger.info('=========添加项目接口开始测试==========')
        # 类级前置
        # 1. 注册一个普通用户
        mobile_phone = generate_no_use_phone()
        pwd = '12345678'
        if not register(mobile_phone=mobile_phone, pwd=pwd):
            cls.logger.error('注册普通用户{}失败'.format(mobile_phone))
            raise ValueError('注册普通用户{}失败'.format(mobile_phone))
        cls.logger.info('注册普通用户{}成功'.format(mobile_phone))
        # 2. 登录这个用户
        data = login(mobile_phone=mobile_phone, pwd=pwd)
        if data is None:
            cls.logger.error('登录普通用户{}失败'.format(mobile_phone))
            raise ValueError('登录普通用户{}失败'.format(mobile_phone))
        # 3. 保存需要的数据能够在这个类的生命周期中共享
        # 为了在用例间传递数据，我们讲数据保存在类属性中
        # 要保持普通用户的member_id和token
        cls.normal_member_id = data['id']
        cls.normal_token = data['token_info']['token']
        # 4. 注册一个管理员账户
        mobile_phone = generate_no_use_phone()
        if not register(mobile_phone=mobile_phone, pwd=pwd, _type=0):
            cls.logger.error('注册用户{}失败'.format(mobile_phone))
            raise ValueError('注册用户{}失败'.format(mobile_phone))
        cls.logger.info('注册用户{}成功'.format(mobile_phone))
        # 5. 登录管理员用户
        data = login(mobile_phone=mobile_phone, pwd=pwd)
        if data is None:
            cls.logger.error('登录管理员用户{}失败'.format(mobile_phone))
            raise ValueError('登录管理员用户{}失败'.format(mobile_phone))
        # 6. 保存数据
        # 管理员的token
        cls.token = data['token_info']['token']

    def setUp(self) -> None:
        """
        方法级前置条件，每个测试函数执行 前执行
        :return:
        """
        res = add_loan(member_id=self.normal_member_id, token=self.normal_token)
        if res:
            self.logger.info('添加项目成功！')
            # 保存项目id到类属性中，传递个当前的测试方法
            # 属性名load_id与用例数据中的槽位一致
            self.__class__.loan_id = res['id']
        else:
            self.logger.error('添加项目失败')
            raise ValueError('添加项目失败')

    @data(*cases)
    def test_audit(self, case):
        self.checkout(case)