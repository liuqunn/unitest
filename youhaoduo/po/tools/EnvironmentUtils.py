# -*-coding:utf-8-*-
from po.tools.lib import adbOperation
from po.tools.install import InstallApp, InstallFactory
import platform
import os
system = platform.system()


class Util(object):
    def __init__(self, serial):
        self.serial = serial
        self.adb = adbOperation.ADB(self.serial)
        # self.apk_path = apk_path
        # self.apk_path = os.path.join(root_path, [name for name in os.listdir(root_path) if name.endswith("apk")].pop())

    def install_target_app_new_install(self, apk_path):
        self.remove_target_app()  # 卸载包名相同的Apk,以确保测试apk为本次上传的Apk
        if apk_path:
            brand = self.adb.get_devices_manufacturer()
            InstallFactory.main(self.serial, apk_path, brand)  # 安装应用
        return self.adb.is_install('com.p1.mobile.putong')

    def cover_install_apk(self, apk_path):
        if apk_path:
            brand = self.adb.get_devices_manufacturer()
            InstallFactory.main(self.serial, apk_path, brand)
        return True

    def remove_target_app(self):
        self.adb.remove_app('com.p1.mobile.putong')