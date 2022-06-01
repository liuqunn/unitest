#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import re
from loguru import logger
from po.tools.webauth_cookie import WebAuthCookie
from po.tools.get_webauth_cookie import get_cookies
import json
import os
import urllib
from urllib import request as req
from po import config


def get_version_code(os_name='Android', num='5'):
    """
    获取过去若干版本的版本号[之前5个以发版版本][只取大版本号]
    """
    url = 'http://inspection.p1staff.com/feedback_platform/api/get_tsp_version/?os=%s&num=%s' % (os_name, num)
    # data = {
    #     'os': 'Android',
    #     'num': '5'
    # }
    # data = json.dumps(data)
    cookies = get_cookies()
    # cookies = WebAuthCookie().main()
    r = requests.get(url, cookies=cookies)
    return json.loads(r.text)['detail']


def get_package_path_of_version(version, os_name='Android'):
    if os_name == 'Android':
        # version_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../android_apk/", version))
        version_file_path = os.path.join(config.android_apk_folder_path, version)
    else:
        version_file_path = os.path.join(config.ios_ipa_folder_path, version)
    if os.path.exists(version_file_path):
        file_path = get_file_path_in_project(version_file_path)
        if file_path == '':
            if download_version_file(version, version_file_path, os_name):
                return get_file_path_in_project(version_file_path)
            else:
                return ''
        else:
            return file_path
    else:
        os.makedirs(version_file_path)
        if download_version_file(version, version_file_path, os_name):
            return get_file_path_in_project(version_file_path)
        else:
            return ''


def get_file_path_in_project(version_file_path):
    files = os.listdir(version_file_path)
    files.sort()
    for file in files:
        if 'DS_Store' not in file:
            return os.path.join(version_file_path, file)
    return ''


def download_version_file(version, version_file_path, os_name):
    if os_name == 'Android':
        file_name = version + '.apk'
    else:
        file_name = version + '.ipa'
    dest_dir = os.path.join(version_file_path, file_name)
    detail = get_detail(version, os_name)
    cookies = get_cookies()
    # cookies = WebAuthCookie().main()
    if detail:
        if os_name == 'Android':
            url = 'https://qa.p1staff.com/file/get_file_Android:%s:release:%s' % (version, detail)
        else:
            if file_name != detail:
                version = detail.rsplit('_', 1)[0]
            url = 'https://qa.p1staff.com/file/get_file_iOS:%s:enterprise:%s' % (version, detail)
        try:
            r = requests.get(url, stream=True, cookies=cookies)
            with open(dest_dir, "wb") as code:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        code.write(chunk)
            return True
        except Exception:
            return False
    return False


def get_detail(version, os_name):
    base_url = 'https://qa.p1staff.com/file/get_list'
    cookies = get_cookies()
    # cookies = WebAuthCookie().main()
    r = requests.get(base_url, cookies=cookies)
    result = json.loads(r.text)
    result_name = ''
    if os_name == 'Android':
        if os_name in result:
            if version in result[os_name]:
                if 'release' in result[os_name][version]:
                    return list(result[os_name][version]['release'])[0]
    else:
        max_num = 0
        if os_name in result:
            for k in list(result[os_name].keys()):
                if version in k:
                    if 'enterprise' in result[os_name][k]:
                        for i in list(result[os_name][k]['enterprise']):
                            if 'ipa' in i:
                                this_num = int(i.split('_')[1].split('.')[0])
                                if this_num > max_num:
                                    max_num = this_num
                                    result_name = i
    return result_name


def download_all_package(url):
    for i in get_version_code():
        get_package_path_of_version(i)
    GetApk.get_apk(url)


def download_old_package(version):
    return get_package_path_of_version(version)


def download_new_package(url):
    return GetApk.get_apk(url)


class GetApk(object):
    apk = None

    def send_dingtalk(self, dingtalk_token, down_url):
        '''将结果发送到钉钉
        Returns:

        '''
        dingdingurl = dingtalk_token
        # dingdingurl = 'https://oapi.dingtalk.com/robot/send?access_token=ffc7cc978e07d4e50e136e2671d87fc4f5fba1d00c8ef5d6cc23a24c743b7514'
        headers = {"Content-Type": "application/json;"}

        text = 'Jenkins monkey 开始:' '\n'\
               '本次使用版本: '+ down_url

        data = {
            "msgtype": "text",
            "text": {
                "content": text
            }
        }

        r = requests.post(dingdingurl, data=json.dumps(data), headers=headers)
        logger.info('钉钉发送结果' + r.text)

    @classmethod
    def get_apk(cls, url, dingtalk_token=None):
        session = requests.session()

        jenkins_login_url = 'http://10.192.231.86:8081/j_acegi_security_check'
        data = {
            'j_username': 'server',
            'j_password': '111111'
        }
        session.post(jenkins_login_url, data=data)

        # try:
        os.system('rm -rf %s' % config.lastest_version_apk_folder_path)
        logger.info('开始下载apk: {}'.format(url))
        app_version = re.search(r'debug/(.*apk)', url).group(1)
        if not os.path.exists(config.lastest_version_apk_folder_path):
            os.mkdir(config.lastest_version_apk_folder_path)
        cls.apk = os.path.join(config.lastest_version_apk_folder_path, app_version)
        r = session.get(url, stream=True)
        with open(cls.apk, "wb") as pdf:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
        logger.info('apk下载完成')
        # except Exception as e:
        #     logger.error('apk下载失败!{}'.format(e))
        # try:
        #     cls().send_dingtalk(dingtalk_token, url)
        # except Exception as e:
        #     logger.error('钉钉发送通知失败!{}'.format(e))
        return cls.apk

    @classmethod
    def get_apk_by_mr_system(cls, url):
        """
        通过Android MR系统下载apk包
        :param url: MR系统中的url
        :return:
        """
        # cookies = WebAuthCookie().main()
        cookies = {'token': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjMxNTM2MDAwMDE1OTUyMjU5NTUsImlzcyI6ImxpY2h'
                            'lbmhhbyJ9.Pcayo8YTIc5nIb_pvSLhVVUKTZUs0beAShNbNS-1BNRY6iBDNi783aedF1C5pgFxB29AVQYaX6G8sm'
                            'Y026Em7EdJXIYr2wNu3F0L8QaWCd38lrTPT_h5nL2zOSWYIifO7-tsZR70BazfOyTnb0sBnpKbfyBqum355Pddw4'
                            'KTFxwI4yYTl2loZaMAkqcuWUXih-br663mgqUGKlHFMW29p8rTfkRn9gZ37A9U7QJkHrJZb3XplULJZZb5GkUFSz'
                            'dX0rJbhwTGiMF0HfVfvwoO62e9KZF0nmyXUfKb54Ko8wRscWipGdkpu4vJnEKlypxDdnBfzNpR41S5I8wsSs9ESg',
                   'name': 'lichenhao'}
        os.system('rm -rf %s' % config.lastest_version_apk_folder_path)
        logger.info('开始下载apk: {}'.format(url))
        app_version = re.search(r'/tantan-(.*apk)', url).group(1)[0:5] + '.apk'
        if not os.path.exists(config.lastest_version_apk_folder_path):
            os.mkdir(config.lastest_version_apk_folder_path)
        config.lastest_apk = os.path.join(config.lastest_version_apk_folder_path, app_version)
        cls.apk = os.path.join(config.lastest_version_apk_folder_path, app_version)
        r = requests.get(url, stream=True, cookies=cookies)
        with open(cls.apk, 'wb') as f:
            f.write(r.content)
        logger.info('apk下载完成')
        return cls.apk


if __name__ == '__main__':
    # a = get_package_path_of_version('4.1.1')
    # print(a)
    # for i in get_version_code():
    #     print(i)
    #     print(get_package_path_of_version(i))
    #     print('--------')
    download_all_package('http://10.192.231.86:8081/job/152_android_integration_build/113/artifact/app/build/outputs/apk/localV7/debug/113.apk')
    # GetApk.get_apk('http://10.192.231.86:8081/job/152_android_integration_build/113/artifact/app/build/outputs/apk/localV7/debug/113.apk')
    # print('-----')
    # print(GetApk.apk)
    # print('-----')
