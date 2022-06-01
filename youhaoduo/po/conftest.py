#!/usr/bin/env python
# -*- coding: utf-8 -*-


import pytest
import allure
from appium import webdriver
from po.driver.client import AndroidClient
from po.driver.driver_YouHaoduo import DriverYouHaoduo

def pytest_addoption(parser):
    parser.addoption("--cmdopt", action="store", default="device", help="None")

@pytest.fixture(scope="session")
def cmdopt(request):
    return request.config.getoption("--cmdopt")


@pytest.fixture(scope="session")
def driver(cmdopt):

    device = eval(cmdopt)
    device_caps = {}
    if device["Caps"]["platformName"] == "Android":

        # device_caps["platformVersion"] = getPhoneInfo(device["Caps"]["deviceName"])["release"]
        device_caps["platformName"] = "Android"
        device_caps["automationName"] = "UiAutomator2"
        device_caps["deviceName"] = device["Caps"]['deviceName']
        device_caps["udid"] = device["Caps"]['deviceName']
        device_caps["appPackage"] = "com.smile.gifmaker"
        device_caps["appActivity"] = "com.yxcorp.gifshow.HomeActivity"
        device_caps["noReset"] = True
        # device_caps["noSign"] = True
        device_caps["unicodeKeyboard"] = True
        device_caps["resetKeyboard"] = True
        device_caps["systemPort"] = int(device["systemPort"])
        # remote = "http://127.0.0.1:" + str(device["port"]) + "/wd/hub"
        remote = "http://127.0.0.1:" + str(4723) + "/wd/hub"
        print(f"wo shi pytest {device_caps}")
        # driver = webdriver.Remote(remote, device_caps)
        # return driver
    else:
        # device_caps["platformVersion"] = getPhoneInfo(device["Caps"]["deviceName"])["release"]
        device_caps["platformName"] = "iOS"
        device_caps["automationName"] = "UiAutomator2"
        device_caps["deviceName"] = device["Caps"]['deviceName']
        device_caps["udid"] = device["Caps"]['deviceName']
        device_caps["appPackage"] = "com.smile.gifmaker"
        device_caps["appActivity"] = "com.yxcorp.gifshow.HomeActivity"
        device_caps["noReset"] = True
        # device_caps["noSign"] = True
        device_caps["unicodeKeyboard"] = True
        device_caps["resetKeyboard"] = True
        device_caps["systemPort"] = int(device["systemPort"])
        # remote = "http://127.0.0.1:" + str(device["port"]) + "/wd/hub"
        remote = "http://127.0.0.1:" + str(4723) + "/wd/hub"
        print(f"wo shi pytest {device_caps}")
        # driver = webdriver.Remote(remote, device_caps)
        # return driver
    AndroidClient().restart_app(remote, device_caps)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    try:
        driver = DriverYouHaoduo.driver
        outcome = yield
        rep = outcome.get_result()
        # if rep.when == "call" and rep.failed:
        if rep.when == "call":
            xfail = hasattr(rep, 'wasxfail')
            if (rep.skipped and xfail) or (rep.failed and not xfail):
                f = driver.get_screenshot_as_png()
                allure.attach(f, '失败截图', allure.attachment_type.PNG)
    except:
        pass
