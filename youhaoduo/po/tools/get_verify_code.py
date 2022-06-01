#!/usr/bin/env python



import requests
import re
from loguru import logger
from po.tools.get_webauth_cookie import get_cookies_mod


def pro_verify_code(mobileNumber):
    '''获取正式环境验证码
    Args:
        mobileNumber:

    Returns: 第一个验证码

    '''
    url = 'https://ms-moderation-putong.p1staff.com/account/confirmationcodes'
    data = {
        'countryCode': '93',
        'mobileNumber': mobileNumber
    }
    cookies = get_cookies_mod()
    r = requests.post(url, data=data, cookies=cookies)
    codes = re.findall(r'<td><strong>(.*)</strong></td>', r.text)
    if len(codes) > 0:
        logger.info('%s%s 验证码: %s' %('+93', mobileNumber, codes[0]))
        return codes[0]
    else:
        logger.error('%s%s 查询失败'%('+93',mobileNumber))

def s2_verify_code(mobileNumber):
    '''获取staging2验证码
    Args:
        mobileNumber:

    Returns: 第一个验证码

    '''
    url = 'http://ms-moderation-putong.staging2.p1staff.com/account/confirmationcodes'
    data = {
        'countryCode': '93',
        'mobileNumber': mobileNumber
    }
    cookies = get_cookies_mod()
    r = requests.post(url, data=data, cookies=cookies)
    codes = re.findall(r'<td><strong>(.*)</strong></td>', r.text)
    if len(codes) > 0:
        logger.info('%s%s 验证码: %s' %('+93', mobileNumber, codes[0]))
        return codes[0]
    else:
        logger.error('%s%s 查询失败'%('+93',mobileNumber))