# -*-coding:utf-8-*-

from po.tools.install.InstallApp import InstallApp


class InstallAppOfGoogle(InstallApp):
    def __init__(self, serial, apk_path):
        super().__init__(serial, apk_path)
