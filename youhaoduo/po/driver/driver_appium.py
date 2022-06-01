#!/usr/bin/env python
# -*- coding: utf-8 -*-

from time import sleep
from appium import webdriver


class DriverAppium(object):

    driver = None
    app = "io.appium.settings"
    activity = ".Settings"
    android_udid = ''
    appium_port = '4723'

    def __init__(self):
        if not DriverAppium.driver:
            self.first_start()
        else:
            self.driver.start_activity(self.app, self.activity)

    def first_start(self):
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "huawei"
        caps['udid'] = self.android_udid
        caps["appPackage"] = self.app
        caps["appActivity"] = self.activity
        caps['autoGrantPermissions'] = True
        # caps['unicodeKeyboard']= True
        # caps['resetKeyboard']= True
        caps['noReset'] = True
        caps['automationName'] = 'uiautomator2'

        self.driver = webdriver.Remote("http://localhost:{}/wd/hub".format(self.appium_port), caps)
        self.driver.implicitly_wait(3)
        DriverAppium.driver = self.driver

# a = DriverAppium()
# b = DriverAppium()