#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/9 21:27
# @Author : 心蓝
from unittest.mock import create_autospec

from test_cases.base_case import BaseTest
from common.myddt import ddt, data
from common.fixture import register, login
from common.test_data_handler import (
    generate_no_use_phone,
    get_test_data_from_excel,
)


cases = get_test_data_from_excel(BaseTest.settings.TEST_DATA_FILE, 'recharge')


@ddt
class TestRecharge(BaseTest):
    name = '充值'

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger.info('=========充值接口开始测试==========')
        # 类级前置
        # 1. 注册一个普通用户
        mobile_phone = generate_no_use_phone()
        pwd = '12345678'
        if not register(mobile_phone=mobile_phone, pwd=pwd):
            cls.logger.error('注册用户{}失败'.format(mobile_phone))
            raise ValueError('注册用户{}失败'.format(mobile_phone))
        cls.logger.info('注册用户{}成功'.format(mobile_phone))
        # 2. 登录这个用户
        data = login(mobile_phone=mobile_phone, pwd=pwd)
        if data is None:
            cls.logger.error('登录用户{}失败'.format(mobile_phone))
            raise ValueError('登录用户{}失败'.format(mobile_phone))
        # 3. 保存需要的数据能够在用例中使用
        # 为了在用例间传递数据，我们讲数据保存在类属性中
        cls.member_id = data['id']
        cls.token = data['token_info']['token']

    @data(*cases)
    def test_recharge(self, case):
        self.checkout(case)

    def step(self):
        # 假设第三方支付接口查询地址
        # alipay_url = 'https://www.fastmock.site/mock/8845a245139a327f793421b16e6f63d8/futureloan/alipay'
        # # mock一下发送http请求，mock一下send_http_request
        # # 自定义返回数据，这个要和项目的实际情况结合，实际返回什么，你就要定义什么
        # alipay_mock = create_autospec(self.send_http_request, return_value={"code": 0, "msg": "支付成功"})
        # # 执行mock方法
        # pay_res = alipay_mock(alipay_url, method=self.case['method'], **self.case['request'])
        # alipay_url = 'https://www.fastmock.site/mock/8845a245139a327f793421b16e6f63d8/futureloan/alipay'
        # pay_res = self.send_http_request(url=alipay_url, method='post')
        #
        # if not pay_res.json()['code'] == 0:
        #     raise RuntimeError('支付宝支部不成功！')

        super().step()

