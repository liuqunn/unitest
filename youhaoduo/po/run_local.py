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
from po.tools import get_version_and_download_package


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
    while True:
        appium_line = result.stdout.readline().strip().decode()
        logger.info(appium_line)
        time.sleep(1)
        logger.info("---------start_server----------")
        if 'listener started' in appium_line or 'Error: listen' in appium_line:
            logger.info("----start_server_successful----{}".format(port))
            return port


def stop_server(port):
    # mac
    cmd = "lsof -i :{0}".format(port)
    plist = os.popen(cmd).readlines()
    plisttmp = plist[-1].split()
    logger.info(plisttmp)
    logger.info(plisttmp[1])
    os.popen("kill -9 {0}".format(plisttmp[1]))


def run_pytest(case, device, url):
    # appium_port = start_appium()
    # systemPort = str(random.randint(8200, 8299))
    # DriverYouHaoduo.appium_port = appium_port
    # DriverYouHaoduo.systemPort = systemPort
    version = get_version_and_download_package.get_version_code()[0]  # 获取最近的5个版本，安卓为5个全量版本，返回list
    old_app_file_path = get_version_and_download_package.download_old_package(version)  # 根据版本号下载旧包，并返回存储在本机的地址
    latest_app_file_path = get_version_and_download_package.download_new_package(url)  # 根据URL下载旧包并获得存储在本机的地址
    DriverYouHaoduo.android_udid = device
    DriverYouHaoduo.old_app_file_path = old_app_file_path  # 旧包在本机的地址
    DriverYouHaoduo.latest_app_file_path = latest_app_file_path  # 新包在本机的地址
    logger.info(f"cmdopt is {device}")
    report = f"report-{device}"
    try:
        os.system(f"rm -rf ../{report}")
        time.sleep(1)
        logger.info(f"{report} report deleted")
    except:
        logger.info("no directory existed")
    finally:
        logger.info(f"pool run device is {device}")
    pytest.main(["-s", *case, f"--cmdopt={device}", "--alluredir", f"../{report}/xml"])
    time.sleep(1)
    os.system(f"allure generate ../{report}/xml -o ../{report}/html --clean")
    # stop_server(appium_port)
    # stop_server(systemPort)


def runner_pool(case_list, device_list):
    pool = Pool(len(get_devices()))
    pool.map(run_pytest, case_list, device_list)
    pool.close()
    pool.join()


if __name__ == '__main__':
    # run_pytest(['testcases_new/test_exp_01/test_install/test_001_first_install_and_cover_install/test_001_old_apk_tel_sign_in_and_cover_install.py', ], '69a7257b',
    #            'http://10.192.231.86:8081/job/152_android_integration_build/113/artifact/app/build/outputs/apk/localV7/debug/113.apk')
    run_pytest(['testcases_new/test_01_signup_signin',], '66J0218B12013259',
               'http://10.192.231.86:8081/job/152_android_integration_build/146/artifact/app/build/outputs/apk/localV7/debug/146.apk')
    #
    # run_pytest('testcases/test_012_push', '6HJ4C20331000045')
    # run_pytest('testP0cases', 'Q5S5T19527015958')
    # run_pytest(['testcases_new/test_exp_01/test_install/test_001_first_install_and_cover_install/test_001_old_apk_tel_sign_in_and_cover_install.py', ], '69a7257b',
    #            'http://10.192.231.86:8081/job/152_android_integration_build/113/artifact/app/build/outputs/apk/localV7/debug/113.apk')
    # run_pytest('testcases/my_test_001.py', 'NAB0220317000292')
    # run_pytest('testcases/test_001_register_login', 'Q5S5T19527015958')
    # run_pytest('testcases/test_002_pic_verify', 'Q5S5T19527015958')
    # run_pytest('testcases/test_005_main_page', 'Q5S5T19527015958')
    # run_pytest('testcases/test_006_friends_circle', 'Q5S5T19527015958')
    # run_pytest('testcases/test_007_setting_page', 'Q5S5T19527015958')
    # run_pytest('testcases/test_008_personal_info', 'Q5S5T19527015958')
    # run_pytest('testcases/test_009_tantan_coins', 'Q5S5T19527015958')
    # run_pytest('testcases/test_010_chat_page', 'Q5S5T19527015958')
