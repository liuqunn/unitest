#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/19 21:25
# @Author : 心蓝
import json

from test_cases.base_case import BaseTest
from common.test_data_handler import get_test_data_from_excel
from common.myddt import ddt, data
from common.encrypt_handler import generate_sign

cases = get_test_data_from_excel(BaseTest.settings.TEST_DATA_FILE, 'invest')


@ddt
class TestInvest(BaseTest):
    name = '投资'

    @data(*cases)
    def test_invest(self, case):
        self.checkout(case)

    def step(self):
        """
        要用v3版本
        :return:
        """
        if self.case['request']['headers']['X-Lemonban-Media-Type'] == 'lemonban.v3':
            # 因为发送请求在预处理的后面，所以对应的token一定会被替换到headers中
            token = self.case['request']['headers']['Authorization'].split(' ')[-1]
            sign, timestamp = generate_sign(token, self.settings.SERVER_RSA_PUB_KEY)
            # 要添加到json格式的请求体中(根据实际情况的格式来)
            self.case['request']['json']['sign'] = sign
            self.case['request']['json']['timestamp'] = timestamp

        super().step()
        # try:
        #     self.response = self.send_http_request(url=self.case['url'], method=self.case['method'], **self.case['request'])
        # except Exception as e:
        #     self.logger.exception('用例【{}】发送http请求错误'.format(self.case['title']))
        #     self.logger.debug('url:{}'.format(self.case['url']))
        #     self.logger.debug('method:{}'.format(self.case['method']))
        #     self.logger.debug('args:{}'.format(self.case['request']))
        #     raise e

    def assert_db_true(self):
        """
        多条sql的校验
        :return:
        """
        if self.case.get('sql'):

            sqls = json.loads(self.case['sql'])
            for sql in sqls:
                # 查数据库
                try:
                    db_res = self.db.exist(sql)
                    self.assertTrue(db_res)
                except Exception as e:
                    self.logger.exception('用例【{}】数据库断言失败'.format(self.case['title']))
                    self.logger.debug('执行的sql是:{}'.format(sql))
                    raise e

            self.logger.info('用例【{}】数据库断言成功'.format(self.case['title']))