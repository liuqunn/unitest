
from selenium import webdriver
from fake_useragent import UserAgent
from outlook import OutLook
from twitch import Twitch
from comm import Comm


class TwitchDriver:
    def __init__(self):
        # 进入浏览器设置
        options = webdriver.ChromeOptions()
        #解决报错 returned -1, SSL error code 1, net_error -100
        options.add_argument('--ignore-certificate-errors') 
        options.add_argument('--ignore-ssl-errors')
        options.add_experimental_option('excludeSwitches',['enable-automation'])
        
        #随机请求头
        options.add_argument('--disable-gpu')
        user_agent = UserAgent().chrome
        options.add_argument('user-agent=%s'%user_agent)
        
        # # 创建浏览器对象
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(120)
        print(self.driver)
        
    def outlok(self):
        return OutLook(self.driver)
    
    def twit(self):
        return Twitch(self.driver)
    
    def comm(self):
        return Comm(self.driver)

if __name__ == '__main__':
    TwitchDriver()