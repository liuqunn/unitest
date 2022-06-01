#!/usr/bin/env python


import requests
import re


class WebAuthCookie(object):

    def __init__(self, username, password, url="https://confluence.p1staff.com/"):
        '''
        Args:
            username:
            password:
            url: 默认从confluence重定向登录
        '''
        self.url = url
        self.username = username
        self.password = password


    def get_rt_st(self):
        '''获取重定向地址
        Returns: 重定向地址

        '''

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3980.0 Safari/537.36',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode':'navigate'
        }

        r = requests.get(self.url,verify=False,allow_redirects=False)
        # 重定向地址
        location = r.headers['location']
        return location


    def webauth_login(self, location):
        '''登录和获取cookie
        Args:
            location: 重定向地址

        Returns: cookies dict

        '''
        # webauth_url = re.search(r'(http.*/)?', location).group(1)
        webauth_url = 'https://webkdc.p1staff.com/login'
        RT = re.search(r'RT=(.*);ST', location).group(1)
        ST = re.search(r'ST=(.*)', location).group(1)
        data = {
            'rm': 'index',
            'RT': RT,
            'ST': ST,
            'login': 'yes',
            'username': self.username,
            'password': self.password,
            'remember_login': 'yes',
            'Submit': 'Login/登录'
        }

        r1 = requests.post(webauth_url, data=data, verify=False)
        redirect = re.findall(r'content="(https.*);"', r1.text)[0]

        # 增加失败重试机制

        for i in range(20):
            r2 = requests.get(redirect, verify=False, allow_redirects=False)
            location2 = r2.headers['location']
            if not str(location2).startswith('https://webkdc.p1staff.com'):
                break


        # location2 = 'https://webkdc.p1staff.com'
        # while str(location2).startswith('https://webkdc.p1staff.com'):
        #     r2 = requests.get(redirect, verify=False, allow_redirects=False)
        #     location2 = r2.headers['location']

        try:
            set_cookie = r2.headers['set-cookie']
            webauth_at = re.search(r'webauth_at=(.*?);', set_cookie).group(1)
            cookies = {'webauth_at': webauth_at}
            print(cookies)
            return cookies
        except:
            print('获取cookie失败')



    def get_qa(self, cookies):
        '''用于测试
        Args:
            cookies:

        Returns:

        '''
        url = 'https://qa.p1staff.com/file/get_list'
        r = requests.get(url, cookies=cookies, verify=False)
        print(r.text)

    def main(self):
        location = self.get_rt_st()
        cookies = self.webauth_login(location)
        return cookies

    def test(self):
        location = self.get_rt_st()
        cookies = self.webauth_login(location)
        # 下面一行用于测试
        self.get_qa(cookies)
        return cookies


if __name__ == "__main__":
    name = 'xxx'
    passwd = 'xxx'
    # url = "https://qa.p1staff.com/"
    # url = "https://jira.p1staff.com/"
    # url = "https://confluence.p1staff.com/"
    # WebAuthCookie(name, passwd, url).main()

    # 获取cookie
    # WebAuthCookie(name, passwd).main()
    # 获取cookie + 测试
    #WebAuthCookie(name, passwd).test()