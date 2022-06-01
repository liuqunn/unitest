#!/usr/bin/env python

import string
import requests
from loguru import logger
from po.tools.get_webauth_cookie import get_cookies, get_cookies_mod


cookies = get_cookies()
cookies_mod = get_cookies_mod()

def get_uid(tel):
    '''通过手机号获取uid
    Args:
        tel:

    Returns: uid

    '''
    url = 'https://ms-vip-admin.p1staff.com/api/users/+93{}'.format(tel)
    r = requests.get(url, cookies=cookies)
    # logger.info(r.text)
    if r.text.startswith('{"clo'):
        if r.json()['user']['mobile']['countryCode'] == 93 and r.json()['user']['mobile']['number'] == tel:
            uid = r.json()['user']['id']
            logger.info('获取uid成功，手机号: +93 {}, uid: {}'.format(tel, uid))
            return uid
        else:
            logger.error('获取uid失败, 不是93')
            raise
    else:
        logger.error('获取uid失败')
        raise

def get_uid_s2(tel):
    '''通过手机号获取uid
    Args:
        tel:

    Returns: uid

    '''
    url = 'http://vip-admin.staging2.p1staff.com/api/users/{}'.format(tel)
    r = requests.get(url)
    # logger.info(r.text)
    if r.text.startswith('{"clo'):
        if r.json()['user']['mobile']['countryCode'] == 93 and r.json()['user']['mobile']['number'] == tel:
            uid = r.json()['user']['id']
            logger.info('获取uid成功，手机号: +93 {}, uid: {}'.format(tel, uid))
            return uid
        else:
            logger.error('获取uid失败, 不是93')
            raise
    else:
        logger.error('获取uid失败')
        raise

def get_uid_name(name):
    '''通过name获取uid
    Args:
        name:

    Returns: uid

    '''
    url = 'https://ms-moderation-putong.p1staff.com/search?q={}'.format(name)
    r = requests.get(url, cookies=cookies_mod, allow_redirects=False)
    logger.info(r.headers)
    if 'Location' in r.headers:
        uid = r.headers['Location'][7:]
        logger.info('获取uid成功，用户名: {}, uid: {}'.format(name, uid))
        return uid
    else:
        logger.error('获取uid失败')
        raise

def set_good(uid):
    '''把uid改为good
    Args:
        uid:

    Returns:

    '''
    url = 'https://ms-moderation-putong.p1staff.com/users/{}'.format(uid)
    data = {
        "action": "default",
        "stateAction": "",
        "filter": "",
        "area": "",
        "id": uid,
        # "oldStatus": "default",
        "oldStatus": "hidden",
        # "oldStatus": "banned",
        "statusReason": "",
        "muteReason": "",
        "statusMessageKey": "",
        "muteMessageKey": "",
        "profileKeywords": "[]",
        "currentSelectJob": "",
        "timeCost": "2821",
        "shouldCheckForSpam": "false",
        # "pictureHashes[0]": "14120998329946516969",
        # "profilePictures[0]": "7237280371"
    }
    statuss = ['pending', 'hidden', 'banned']
    for status in statuss:
        data['oldStatus'] = status
        r = requests.post(url, data=data, cookies=cookies_mod, allow_redirects=False)
        if r.text == '':
            logger.info('从{}设置good成功'.format(status))
        else:
            logger.error('从{}设置good失败'.format(status))

def set_good_s2(uid):
    '''把uid改为good
    Args:
        uid:

    Returns:

    '''
    url = 'http://ms-moderation-putong.staging2.p1staff.com/users/{}'.format(uid)
    data = {
        "action": "default",
        "stateAction": "",
        "id": uid,
        "oldStatus": "hidden",
        "statusReason": "",
        "muteReason": ""
    }
    statuss = ['pending', 'hidden', 'banned']
    for status in statuss:
        data['oldStatus'] = status
        r = requests.post(url, data=data, allow_redirects=False)
        if r.text == '':
            logger.info('从{}设置good成功'.format(status))
        else:
            logger.error('从{}设置good失败'.format(status))

def set_banned(uid):
    '''把uid改为banned
    Args:
        uid:

    Returns:

    '''
    url = 'https://ms-moderation-putong.p1staff.com/users/{}'.format(uid)
    data = {
        "action": "banned",
        "stateAction": "",
        "filter": "",
        "area": "",
        "id": uid,
        "oldStatus": "hidden",
        "statusReason": "",
        "muteReason": "",
        "statusMessageKey": "",
        "muteMessageKey": "",
        "profileKeywords": "[]",
        "currentSelectJob": "",
        "timeCost": "2821",
        "shouldCheckForSpam": "false",
        # "pictureHashes[0]": "14120998329946516969",
        # "profilePictures[0]": "7237280371"
    }
    statuss = ['pending', 'hidden', 'default']
    for status in statuss:
        data['oldStatus'] = status
        r = requests.post(url, data=data, cookies=cookies_mod, allow_redirects=False)
        if r.text == '':
            logger.info('从{}设置banned成功'.format(status))
        else:
            logger.error('从{}设置banned失败'.format(status))

def set_staff(uid):
    '''把uid用户设置为员工
    Args:
        uid:

    Returns:

    '''
    url = 'https://ms-moderation-putong.p1staff.com/users/{}/staff'.format(uid)
    data = {
        'isStaff': 'on'
    }
    r = requests.post(url, data=data, cookies=cookies_mod, allow_redirects=False)
    if r.text == '':
        logger.info('设置员工成功')
    else:
        logger.error('设置员工失败')
        raise

def del_uid(uid):
    '''根据uid删除用户
    Args:
        uid:

    Returns:

    '''
    # url = 'http://ms-moderation-putong.staging1.p1staff.com/account/deleteaccount'
    url = 'https://ms-moderation-putong.p1staff.com/account/deleteaccount'
    data = {
        'userId': uid
    }
    r = requests.post(url, data=data, cookies=cookies_mod)
    if '<p class="third-party-status-default">Success</p>' in r.text:
        logger.info('删除成功, uid: {}'.format(uid))
    else:
        logger.error('删除失败')
        raise

def num_to_a(num):
    alpha_dict = dict(enumerate(string.ascii_lowercase[:10]))
    a = ''
    for i in str(int(num)):
        a = a + alpha_dict[int(i)]
    logger.info('{} to {}'.format(num, a))
    return a

def set_good_tel(tel):
    uid = get_uid(tel)
    set_good(uid)

def set_good_tel_s2(tel):
    uid = get_uid_s2(tel)
    set_good_s2(uid)

def set_banned_tel(tel):
    uid = get_uid(tel)
    set_banned(uid)

def set_banned_name(name):
    uid = get_uid_name(name)
    set_banned(uid)

def del_user_tel(tel):
    uid = get_uid(tel)
    set_staff(uid)
    del_uid(uid)

def del_user_name(name):
    uid = get_uid_name(name)
    set_staff(uid)
    del_uid(uid)