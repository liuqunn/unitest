# -*-coding:utf-8-*-

from po.tools.install import InstallAppOfXiaoMi
from po.tools.install import InstallAppOfGoogle, InstallAppOfHuaWei
import multiprocessing

event = multiprocessing.Event()

install_switch = {
    "xiaomi": InstallAppOfXiaoMi.InstallAppOfXiaoMi,
    "huawei": InstallAppOfHuaWei.InstallAppOfHuaWei,
    "google": InstallAppOfGoogle.InstallAppOfGoogle
}


def tap_window(ia):
    event.set()
    ia.tap_popup_windows(event)


def install_app(ia):
    ia.install_app()
    event.clear()


def due_brand(brand):
    deviceBrand = brand.lower().strip()
    flag = False
    print("deviceBrand:", deviceBrand)
    for br in list(install_switch.keys()):
        if br in deviceBrand:
            flag = True
            break
    if not flag:
        deviceBrand = "google"
    # if deviceBrand not in list(install_switch.keys()):
    #     deviceBrand = 'google'
    return deviceBrand


def main(serial, apk_path, brand):
    devicebrand = due_brand(brand)
    install = install_switch.get(devicebrand)(serial, apk_path)
    pool = multiprocessing.Pool(2)
    pool.apply_async(tap_window, [install])
    pool.apply_async(install_app, [install])
    pool.close()
    pool.join()
