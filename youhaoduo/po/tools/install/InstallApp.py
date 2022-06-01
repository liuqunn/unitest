# -*-coding:utf-8-*-
import time
import xml.etree.ElementTree as elementtree
import re
import os
import copy
from po.tools.lib import adbOperation
from po import config


class InstallApp(object):
    def __init__(self, serial, apk_path):
        self.serial = serial
        self.apk_path = apk_path
        self.data_path = os.path.join(config.install_app_dump_file_path)
        self.adb = adbOperation.ADB(self.serial)
        self.__button_list = []

    def set_button_list(self, button_list):
        self.__button_list = copy.deepcopy(button_list)

    def install_app(self):
        # self.adb.quit_app("com.android.packageinstaller")
        self.adb.install_app(self.apk_path).communicate()
        # event.clear()

    def tap_popup_windows(self, event):
        queue = []
        while len(queue) < 20 and event.is_set():
            coordinate_points = self.element()
            if coordinate_points is not None:
                self.adb.touch_by_element(coordinate_points)
            time.sleep(2)
            queue.append(1)

    def element(self):
        ui_dump_path = os.path.join(self.data_path, "ui_dump.xml")
        self.adb.get_focused_package_xml(ui_dump_path)
        if os.path.exists(ui_dump_path):
            pattern = re.compile(r"\d+")
            tree = elementtree.ElementTree(file=ui_dump_path)
            tree_iter = tree.iter(tag="node")
            for elem in tree_iter:
                # print elem.attrib["resource-id"]
                if elem.attrib["resource-id"] in self.__button_list:
                    bounds = elem.attrib["bounds"]
                    coord = pattern.findall(bounds)
                    x_point = (int(coord[2]) - int(coord[0])) / 2.0 + int(coord[0])
                    y_point = (int(coord[3]) - int(coord[1])) / 2.0 + int(coord[1])
                    return x_point, y_point




