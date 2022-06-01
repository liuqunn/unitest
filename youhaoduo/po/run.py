#!/usr/bin/env python
# -*- coding: utf-8 -*-



import os
import sys
sys.path.append(os.getcwd())
import time
import pytest
import random
# from multiprocessing import Pool
from pathos.multiprocessing import ProcessingPool as Pool  # 支持多参数
import subprocess
from loguru import logger
from po.driver.driver_YouHaoduo import DriverYouHaoduo


def get_devices():
    # 检查设备
    # result = self.call_adb("devices")
    devices = []
    result = subprocess.Popen("adb devices", shell=True, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE).stdout.readlines()

    for item in result:
        t = item.decode().split("\tdevice")
        if len(t) >= 2:
            devices.append(t[0])
    # print(result)
    # print(devices)
    return devices


def get_phone_info(device):
    cmd = "adb -s " + device + " shell cat /system/build.prop "
    logger.info(cmd)
    # phone_info = os.popen(cmd).readlines()
    phone_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    result = {"release": "5.0", "model": "model2", "brand": "brand1", "device": "device1"}
    release = "ro.build.version.release="  # 版本
    model = "ro.product.model="  # 型号
    brand = "ro.product.brand="  # 品牌
    device = "ro.product.device="  # 设备名
    for line in phone_info:
        for i in line.split():
            temp = i.decode()
            if temp.find(release) >= 0:
                result["release"] = temp[len(release):]
                break
            if temp.find(model) >= 0:
                result["model"] = temp[len(model):]
                break
            if temp.find(brand) >= 0:
                result["brand"] = temp[len(brand):]
                break
            if temp.find(device) >= 0:
                result["device"] = temp[len(device):]
                break
    print(result)
    return result


def devices_list():
    devices_list = []
    for i in range(0, len(get_devices())):
        _initApp = {}
        _initCaps = {}
        _initApp["devices"] = get_devices()[i]
        _initCaps["deviceName"] = get_devices()[i]
        # _initCaps["platformVersion"] = getPhoneInfo(devices=_initCaps["deviceName"])["release"]
        _initCaps["platformName"] = "Android"
        # _initApp["port"] = str(random.randint(4700, 4900))
        # _initApp["bport"] = str(random.randint(4700, 4900))
        _initApp["systemPort"] = str(random.randint(4700, 4900))
        # _initCaps["automationName"] = "UiAutomator2"
        # _initCaps["appPackage"] = 'cn.vsx.vc'
        # _initCaps["appActivity"] = '.activity.RegistActivity'
        _initApp["Caps"] = _initCaps
        devices_list.append(_initApp)
    print(len(devices_list))
    return devices_list


def start_appium():
    port = str(random.randint(4700, 4900))
    cmd = "appium -p {} --relaxed-security --log-timestamp --local-timezone".format(port)
    logger.info(cmd)
    result = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for i in range(30):
        appium_line = result.stdout.readline().strip().decode()
        logger.info(appium_line)
        time.sleep(0.5)
        logger.info("---------start_server----------")
        if 'listener started' in appium_line or 'Error: listen' in appium_line:
            logger.info("----start_server_successful----{}".format(port))
            return port


def stop_server(port):
    # mac
    try:
        cmd = "lsof -i :{0}".format(port)
        plist = os.popen(cmd).readlines()
        plisttmp = plist[-1].split()
        logger.info(plisttmp)
        logger.info(plisttmp[1])
        os.popen("kill -9 {0}".format(plisttmp[1]))
        time.sleep(2)
    except:
        logger.error('未查找到相关进程')

def run_pytest(case, device):
    appium_port = start_appium()
    systemPort = str(random.randint(8200, 8299))
    logger.info(systemPort)
    DriverYouHaoduo.appium_port = appium_port
    DriverYouHaoduo.systemPort = systemPort
    DriverYouHaoduo.android_udid = device
    logger.info(f"cmdopt is {device}")
    # report = f"report-{device}"
    report = "report"
    try:
        os.system(f"rm -rf ../{report}")
        time.sleep(1)
        logger.info(f"{report} report deleted")
    except:
        logger.info("no directory existed")
    finally:
        logger.info(f"pool run device is {device}")
    pytest.main(["-s", case, "--alluredir", f"{report}/xml"])
    time.sleep(1)
    # os.system(f"allure generate {report}/xml -o {report}/html --clean")
    stop_server(appium_port)
    # stop_server(systemPort)


def runner_pool(case_list, device_list):
    pool = Pool(len(get_devices()))
    pool.map(run_pytest, case_list, device_list)
    pool.close()
    pool.join()


if __name__ == '__main__':
    cases = sys.argv[1]
    device = sys.argv[2]
    run_pytest(cases, device)
    # run_pytest('po/testcases/test_006_friends_circle', 'Q5S5T19527015958')
    # run_pytest('po/testP0cases/test_001_publictech/test_002_tel_login.py', '69a7257b')

# python po/run.py po/testcases/test_006_friends_circle Q5S5T19527015958
