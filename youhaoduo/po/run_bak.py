#!/usr/bin/env python


import os
import sys
sys.path.append(os.getcwd())
import time
import pytest
import random
# from multiprocessing import Pool
from pathos.multiprocessing import ProcessingPool as Pool  #支持多参数
import subprocess

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
    cmd = "adb -s " + device +" shell cat /system/build.prop "
    print(cmd)
    # phone_info = os.popen(cmd).readlines()
    phone_info = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout.readlines()
    result = {"release": "5.0", "model": "model2", "brand": "brand1", "device": "device1"}
    release = "ro.build.version.release=" # 版本
    model = "ro.product.model=" #型号
    brand = "ro.product.brand=" # 品牌
    device = "ro.product.device=" # 设备名
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
                result["device"] = temp[len(device) :]
                break
    print(result)
    return result
# get_phone_info("192.168.2.198:15013")

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


def run_pytest(case, device):
    print(f"cmdopt is {device}")
    report = f"report-{device['Caps']['deviceName']}".split(":", 1)[0]
    try:
        os.system(f"rm -rf ../{report}")
        time.sleep(1)
        # os.system(f"rd /s /q E:\\appium-pytest\\{report}")
        # time.sleep(1)
        print(f"{report} report deleted")
    except:
        print("no directory existed")
    finally:
        print(f"pool run device is {device['devices']}")
    pytest.main(["-s", case, f"--cmdopt={device}", "--alluredir", f"../{report}/xml"])
    time.sleep(1)
    os.system(f"allure generate ../{report}/xml -o ../{report}/html --clean")

def runner_pool(case_list, device_list):
    pool = Pool(len(get_devices()))
    pool.map(run_pytest, case_list, device_list)
    pool.close()
    pool.join()

if __name__ == '__main__':
    # 全量执行
    runner_pool(["testcases/test_login.py"], devices_list())
    # 均衡
    # runner_pool(["testcases/test_login.py"], devices_list())
