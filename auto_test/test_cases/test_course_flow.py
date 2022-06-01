#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/4/16 21:27
# @Author : 心蓝
from test_cases.base_case import BaseTest
from common.myddt import ddt, data

cases = [
    {'title': '课堂派登录',
     'method': 'post',
     'url': 'https://v4.ketangpai.com/UserApi/login',
     'request': '{"data": {"email": "877649301@qq.com", "password": "Pythonxinlan", "remember": 0}}',
     'status_code': 200,
     'expect_data': '{"status": 1}'
     },
    {'title': '获取所有课程信息',
     'method': 'get',
     'url': 'https://v4.ketangpai.com/CourseApi/lists',
     'request': '{}',
     'status_code': 200,
     'expect_data': '{"status": 1}'
     },
]


@ddt
class TestCourseFlow(BaseTest):
    name = '课堂派业务流'

    @data(*cases)
    def test_course(self, case):
        self.checkout(case)

    def assert_json_response(self):
        """
        断言json响应数据，xml，html
        :return:
        """
        response_data = self.response.json()
        # 注意这里的逻辑写死了，是针对前程贷这个项目
        # 根据实际项目改写
        # 1. 拼装实际结果字典
        res = {'status': response_data['status']}
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