# -*-coding:utf-8-*-
from po.tools.install.InstallApp import InstallApp


class InstallAppOfXiaoMi(InstallApp):

    def __init__(self, serial, apk_path):
        super().__init__(serial, apk_path)

    def element(self):
        button0 = "android:id/button2"
        button_list = [button0]
        self.set_button_list(button_list)
        return super().element()



