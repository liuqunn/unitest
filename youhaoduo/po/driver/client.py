#!/usr/bin/env python
# -*- coding: utf-8 -*-


from appium import webdriver
from appium.webdriver.webdriver import WebDriver
import yaml

class AndroidClient(object):

    driver:WebDriver
    platform="android"
    @classmethod
    def install_app(cls) -> WebDriver:

        caps = {}
        #如果有必要，进行第一次安装
        # caps["app"]=''
        caps["platformName"] = "android"
        caps["deviceName"] = "mi"
        caps["appPackage"] = "com.smile.gifmaker"
        caps["appActivity"] = "com.yxcorp.gifshow.HomeActivity"
        #解决第一次启动的问题
        caps["autoGrantPermissions"] = "true"
        # caps['noReset']=True

        cls.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        cls.driver.implicitly_wait(10)
        return cls.driver


    @classmethod
    def restart_app(cls, url, caps) -> WebDriver:
        # caps = {}
        #
        # caps["platformName"] = "android"
        # caps["deviceName"] = "mi"
        # caps["appPackage"] = "com.smile.gifmaker"
        # caps["appActivity"] = "com.yxcorp.gifshow.HomeActivity"
        # #为了更快的启动，并保留之前的数据，从而可以保存上一个case执行后的状态
        # caps['noReset']=True
        # # caps['chromedriverExecutableDir']="/Users/projects/chromedriver/2.20"
        # caps['unicodeKeyboard']=True
        # caps['resetKeyboard']=True
        # #caps["udid"]="emulator-5554"
        # # caps['udid'] = udid,
        # # caps['systemPort'] = systemPort,
        # caps['dontStopAppOnReset']=True
        # caps['automationName']='UiAutomator2'
        # url = "http://localhost:4723/wd/hub"


        cls.driver = webdriver.Remote(url, caps)
        cls.driver.implicitly_wait(3)
        return cls.driver


