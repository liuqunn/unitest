import time,random,os,threading
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support  import expected_conditions as EC
from comm import *
import xlrd as xr
from fake_useragent import UserAgent


class chromeDriver:
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
        
    def open_Js(self,url):
        js = f'window.open({url});'
        self.driver.execute_script(js)
        
    def open_browser(self,url):
        self.driver.get(url)
    
    def switch_handle(self):
        # 对窗口进行遍历
        handle = self.driver.current_window_handle
        handles = self.driver.window_handles
        for newhandle in handles:
            # 筛选新打开的窗口B
            if newhandle!=handle:
                # 切换到新打开的窗口B
                self.driver.switch_to.window(newhandle)
                
            
    def close_chrome(self,min):
        time.sleep(15)
        self.driver.minimize_window()
        time.sleep(min*60)
        self.driver.quit()
        
    #切换到指定frame
    def switch_frame(self,fram_xpath):
        # WebDriverWait(self.driver,120,0.5).until(EC.frame_to_be_available_and_switch_to_it(fram_xpath))
        self.driver.switch_to_frame(fram_xpath)
        
    #切换到默认的frame
    def defult_frame(self):
        self.driver.switch_to.default_content()
        
    def judgEle(self,eleXpath):
        try:
            WebDriverWait(self.driver,20).until(EC.invisibility_of_element_located((By.XPATH,eleXpath)))
            return True
        except:
            return False