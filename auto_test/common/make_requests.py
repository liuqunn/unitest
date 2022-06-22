#! /usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2021/3/24 20:02
# @Author : 心蓝

"""
发送请求

需求：
1. 根据用例发送对应方法(get,post...)的http请求
2. 能够动态的接受不同的请求参数 json，params，data，headers，cookies
"""
import requests


def send_http_request(url, method, **kwargs) -> requests.Response:
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
    return getattr(requests, method)(url=url, **kwargs)


    # if method == 'get':
    #     res = requests.get(url=url, params=params, json=json, data=data, headers=headers, cookies=cookies)
    # elif method == 'post':
    #     res = requests.post(url=url, params=params, json=json, data=data, headers=headers, cookies=cookies)
    # elif method == 'put':
    #     res = requests.put(url=url, params=params, json=json, data=data, headers=headers, cookies=cookies)
    # elif method == 'patch':
    #     res = requests.patch(url=url, params=params, json=json, data=data, headers=headers, cookies=cookies)
    # elif method == 'delete':
    #     res = requests.delete(url=url, params=params, json=json, data=data, headers=headers, cookies=cookies)
    #
    # return res


if __name__ == '__main__':
    """这里的代码只有直接执行当前脚本的时候才会执行"""
    case = {
        'id': 1,
        'title': '注册成功-不带昵称和类型',
        'method': 'post',
        'url': 'http://api.lemonban.com/futureloan/member/register',
        'headers': {"X-Lemonban-Media-Type": "lemonban.v1"},
        'request_data': {"mobile_phone": "15873000001", "pwd": "12345678"},
        'expect_data': {"code": 0, "msg": "OK"}
    }
    res = send_http_request(url=case['url'], method=case['method'], headers=case['headers'], json=case['request_data'])
    print(res.json())
    print(res.text)