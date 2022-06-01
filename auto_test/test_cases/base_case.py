#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/12 21:45
# @Author : 心蓝
import json
import unittest

import requests
from jsonpath import jsonpath

import settings
from common import logger, db
from common.make_requests import send_http_request
from common.test_data_handler import (
    replace_args_by_re,
    generate_no_use_phone
)


class BaseTest(unittest.TestCase):
    name = 'base用例'  # 这个属性应该被覆盖
    logger = logger
    db = db
    settings = settings

    # 会话对象
    session = requests.session()

    @classmethod
    def setUpClass(cls) -> None:
        cls.logger.info('========={}接口开始测试=========='.format(cls.name))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.logger.info('**********{}接口测试结束**********'.format(cls.name))

    def checkout(self, case):
        # 绑定对象属性，便于下面的测试流程函数去处理
        self.logger.info('用例【{}】开始测试>>>>>>>'.format(case['title']))
        self.case = case
        # 1. 测试数据处理
        self.pre_test_data()
        # 2. 测试步骤
        self.step()
        # 3. 响应状态码断言
        self.assert_status_code()
        # 4. 响应数据断言
        self.assert_json_response()
        # 5. 数据库断言
        self.assert_db_true()
        # 6. 提取数据
        self.extract_data()
        self.logger.info('用例【{}】测试结束<<<<<<<<'.format(case['title']))

    def pre_test_data(self):
        """
        预处理数据
        :return:
        """
        # 1. 用例数据处理
        # 替换数据

        self.case['request'] = replace_args_by_re(self.case['request'], self)
        # 替换sql
        if self.case.get('sql'):
            self.case['sql'] = replace_args_by_re(self.case['sql'], self)

        # 判断是否要生成手机号码
        if '#phone#' in self.case['request']:
            # 要动态生成手机号码
            phone = generate_no_use_phone()
            # 替换槽位
            self.case['request'] = self.case['request'].replace('#phone#', phone)
            # 替换sql
            if self.case.get('sql'):
                self.case['sql'] = self.case['sql'].replace('#phone#', phone)

        # 将json字符串转换为python对象
        try:
            self.case['request'] = json.loads(self.case['request'])
            self.case['expect_data'] = json.loads(self.case['expect_data'])
        except Exception as e:
            self.logger.exception('用例【{}】的json格式不正确'.format(self.case['title']))
            self.logger.debug('case["request"]:{}'.format(self.case['request']))
            self.logger.exception('case["expect_data"]:{}'.format(self.case['expect_data']))
            raise ValueError('用例【{}】的json格式不正确'.format(self.case['title']))

        # 判断一下url是否是全路径
        if not self.case['url'].startswith('http'):
            # 拼接url
            self.case['url'] = settings.PROJECT_HOST + settings.INTERFACES[self.case['url']]

    def step(self):
        """
        测试步骤
        :return:
        """
        try:
            self.response = self.send_http_request(url=self.case['url'], method=self.case['method'], **self.case['request'])
        except Exception as e:
            self.logger.exception('用例【{}】发送http请求错误'.format(self.case['title']))
            self.logger.debug('url:{}'.format(self.case['url']))
            self.logger.debug('method:{}'.format(self.case['method']))
            self.logger.debug('args:{}'.format(self.case['request']))
            raise e

    def assert_status_code(self):
        """
        响应状态码断言
        :return:
        """
        try:
            self.assertEqual(self.case['status_code'], self.response.status_code)
        except AssertionError as e:
            self.logger.exception('用例【{}】状态码断言失败！'.format(self.case['title']))
            raise e
        else:
            self.logger.info('用例【{}】状态码断言成功！'.format(self.case['title']))

    def assert_json_response(self):
        """
        断言json响应数据，xml，html
        :return:
        """
        response_data = self.response.json()
        # 注意这里的逻辑写死了，是针对前程贷这个项目
        # 根据实际项目改写
        # 1. 拼装实际结果字典
        res = {'code': response_data['code'], 'msg': response_data['msg']}
        # 2. 断言
        try:
            self.assertEqual(self.case['expect_data'], res)
        except AssertionError as e:
            self.logger.exception('用例【{}】请求json结果断言失败！'.format(self.case['title']))
            self.logger.debug('期望数据：{}'.format(self.case['expect_data']))
            self.logger.debug('实际结果: {}'.format(res))
            self.logger.debug('响应结果：{}'.format(response_data))
            raise e
        else:
            self.logger.info('用例【{}】请求json结果断言成功！'.format(self.case['title']))

    def assert_db_true(self):
        """
        断言数据库存在数据
        :return:
        """
        if self.case.get('sql'):
            # 查询数据
            try:
                db_res = self.db.exist(self.case['sql'])
                self.assertTrue(db_res)
            except Exception as e:
                self.logger.exception('用例【{}】数据库断言失败'.format(self.case['title']))
                self.logger.debug('执行的sql是:{}'.format(self.case['sql']))
                raise e
            else:
                self.logger.info('用例【{}】数据库断言成功'.format(self.case['title']))

    def extract_data(self):
        """
        提取响应中的数据并保存到类属性
        :return:
        """
        if self.case.get('extract'):
            try:
                exps = json.loads(self.case['extract'])
            except Exception as e:
                raise ValueError('用例【{}】的extract提取表达式格式不正确'.format(self.case['title']))
            for item in exps:
                # 要保存的类属性的名称
                name = item['name']
                # 要提取数据的jsonpath表达式
                exp = item['exp']
                res = jsonpath(self.response.json(), exp)

                if res:
                    # 保存到类属性
                    setattr(self.__class__, name, res[0])
                else:
                    raise ValueError('用例【{}】提取表达式错误'.format(self.case['title']), exp)

    def send_http_request(self, url, method, **kwargs) -> requests.Response:
        """
        发送http请求
        :param url:
        :param method:
        :param kwargs: paras,data,json,headers,cookies ...
        :return: response
        """
        # 把方法名小写化，防止误传
        method = method.lower()
        # 获取对应的方法
        return getattr(self.session, method)(url=url, **kwargs)



