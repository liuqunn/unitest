#!/usr/bin/env python
# -*- coding: utf-8 -*-


from time import sleep
from appium import webdriver
from po.pages.base_page import BasePage
from po.pages.guide.first_page import FirstPage
from po.pages.mine.mine_page import MinePage
from po.pages.mine.mall_page import MallPage
from po.pages.recommend.recommend_page import RecommendPage
from po.pages.system.system_page import SystemPage


class DriverYouHaoduo(object):
    driver = None
    app = "com.xi.quickgame.mi"
    activity = "com.xi.quickgame.splash.SplashActivity"
    android_udid = ''
    appium_port = '4723'
    systemPort = '8200'
    old_app_file_path = ''
    latest_app_file_path = ''
    telephone = ''
    username = ''

    def __init__(self):
        if not DriverYouHaoduo.driver:
            print('111')
            # self.hot_start()
            # self.first_page()
        else:
            print('222')
            # self.main_page()
            # print('restart')
            # self.driver.start_activity(self.app, self.activity)

    def first_start(self):
        try:
            self.driver.quit()
        except:
            pass
        caps = {}
        caps["platformName"] = "Android"
        caps["deviceName"] = "hhh"
        caps['udid'] = self.android_udid
        caps['systemPort'] = self.systemPort
        # caps['udid'] = "SCO7HEYSMFDEU4PF"
        caps["appPackage"] = self.app
        caps["appActivity"] = self.activity
        caps['autoGrantPermissions'] = True
        # caps['unicodeKeyboard']= True
        # caps['resetKeyboard']= True
        # caps['noReset'] = True
        caps['automationName'] = 'uiautomator2'
        caps['dontStopAppOnReset'] = False
        caps['newCommandTimeout'] = '3000'

        self.driver = webdriver.Remote("http://localhost:{}/wd/hub".format(self.appium_port), caps)
        self.driver.implicitly_wait(1)
        DriverYouHaoduo.driver = self.driver
        return self

    def first_start_no_permission(self):
        try:
            self.driver.quit()
        except:
            pass
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "hhh"
        caps['udid'] = self.android_udid
        caps['systemPort'] = self.systemPort
        # caps['udid'] = "SCO7HEYSMFDEU4PF"
        caps["appPackage"] = self.app
        caps["appActivity"] = self.activity
        # caps['autoGrantPermissions'] = True
        # caps['unicodeKeyboard']= True
        # caps['resetKeyboard']= True
        # caps['noReset'] = True
        caps['automationName'] = 'uiautomator2'
        caps['dontStopAppOnReset'] = False
        caps['newCommandTimeout'] = '3000'

        self.driver = webdriver.Remote("http://localhost:{}/wd/hub".format(self.appium_port), caps)
        self.driver.implicitly_wait(5)
        DriverYouHaoduo.driver = self.driver
        return self

    def hot_start(self):
        try:
            self.driver.quit()
        except:
            pass
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "dd"
        caps['udid'] = self.android_udid
        caps['systemPort'] = self.systemPort
        # caps['udid'] = "SCO7HEYSMFDEU4PF"
        caps["appPackage"] = self.app
        caps["appActivity"] = self.activity
        caps['autoGrantPermissions'] = True
        # caps['unicodeKeyboard']= True
        # caps['resetKeyboard']= True
        caps['noReset'] = True
        caps['automationName'] = 'uiautomator2'
        caps['dontStopAppOnReset'] = True
        caps['newCommandTimeout'] = '3000'
        # caps["settings"] = {'normalizeTagNames': True}

        self.driver = webdriver.Remote("http://localhost:{}/wd/hub".format(self.appium_port), caps)
        self.driver.implicitly_wait(1)
        sleep(2)
        DriverYouHaoduo.driver = self.driver
        return self

    # 会killAPP 重启app
    def cold_start(self):
        try:
            self.driver.quit()
        except:
            pass
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "hhh"
        caps['udid'] = self.android_udid
        caps['systemPort'] = self.systemPort
        # caps['udid'] = "SCO7HEYSMFDEU4PF"
        caps["appPackage"] = self.app
        caps["appActivity"] = self.activity
        caps['autoGrantPermissions'] = True
        # caps['unicodeKeyboard']= True
        # caps['resetKeyboard']= True
        caps['noReset'] = True
        caps['automationName'] = 'uiautomator2'
        caps['dontStopAppOnReset'] = False
        caps['newCommandTimeout'] = '3000'

        self.driver = webdriver.Remote("http://localhost:{}/wd/hub".format(self.appium_port), caps)
        self.driver.implicitly_wait(1)
        sleep(4)
        DriverYouHaoduo.driver = self.driver
        return self

    def install_start(self):
        try:
            self.driver.quit()
        except:
            pass
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "hhh"
        caps['udid'] = self.android_udid
        caps['systemPort'] = self.systemPort
        caps['app'] = 'http://10.192.231.86:8081/job/android_build/134/artifact/app/build/outputs/apk/local/debug/app-local-debug.apk'
        # caps["appPackage"] = self.app
        # caps["appActivity"] = self.activity
        caps['autoGrantPermissions'] = True
        # caps['unicodeKeyboard']= True
        # caps['resetKeyboard']= True
        caps['noReset'] = True
        caps['automationName'] = 'uiautomator2'
        caps['dontStopAppOnReset'] = False
        caps['newCommandTimeout'] = '3000'

        self.driver = webdriver.Remote("http://localhost:{}/wd/hub".format(self.appium_port), caps)
        self.driver.implicitly_wait(1)
        sleep(4)
        DriverYouHaoduo.driver = self.driver
        return self

    def sim_start(self):
        try:
            self.driver.quit()
        except:
            pass
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "dd"
        caps['udid'] = "Q5S5T19527015958"
        caps['systemPort'] = self.systemPort
        # caps['udid'] = "SCO7HEYSMFDEU4PF"
        caps["appPackage"] = self.app
        caps["appActivity"] = self.activity
        caps['autoGrantPermissions'] = True
        # caps['unicodeKeyboard']= True
        # caps['resetKeyboard']= True
        caps['noReset'] = True
        caps['automationName'] = 'uiautomator2'
        caps['dontStopAppOnReset'] = False
        caps['newCommandTimeout'] = '3000'
        # caps["settings"] = {'normalizeTagNames': True}

        self.driver = webdriver.Remote("http://localhost:{}/wd/hub".format(self.appium_port), caps)
        self.driver.implicitly_wait(1)
        DriverYouHaoduo.driver = self.driver
        return self

    def system_start(self):
        try:
            self.driver.quit()
        except:
            pass
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "hhh"
        caps['udid'] = self.android_udid
        caps['systemPort'] = self.systemPort
        caps["appPackage"] = 'com.android.settings'
        caps["appActivity"] = '.HWSettings'
        caps['autoGrantPermissions'] = True
        # caps['unicodeKeyboard']= True
        # caps['resetKeyboard']= True
        caps['noReset'] = True
        caps['automationName'] = 'uiautomator2'
        caps['dontStopAppOnReset'] = False
        caps['newCommandTimeout'] = '3000'

        self.driver = webdriver.Remote("http://localhost:{}/wd/hub".format(self.appium_port), caps)
        self.driver.implicitly_wait(1)
        # sleep(2)
        DriverYouHaoduo.driver = self.driver
        return self

    def goto_system(self):
        return SystemPage(self.driver)
    def mine_page(self):
        return MinePage(self.driver)
    def recommend_page(self):
        return RecommendPage(self.driver)
    def first_page(self):
        return FirstPage(self.driver)
    def base_page(self):
        return BasePage(self.driver)
    def mall_page(self):
        return MallPage(self.driver)



