# -*-coding:utf-8-*-
from po.tools.install.InstallApp import InstallApp


class InstallAppOfHuaWei(InstallApp):

    def __init__(self, serial, apk_path):
        super().__init__(serial, apk_path)

    def element(self):
        button0 = 'com.android.packageinstaller:id/ok_button'
        button1 = 'com.android.packageinstaller:id/btn_allow_once'
        button2 = 'com.android.packageinstaller:id/bottom_button_two'
        button3 = 'com.android.packageinstaller:id/btn_continue_install'
        button4 = "android:id/button1"
        button5 = 'vivo:id/vivo_adb_install_ok_button'
        button6 = "com.android.vending:id/details_arandroid:id/button1row"
        button7 = "com.android.vending:id/continue_anyway"
        button8 = "com.android.packageinstaller:id/done_button"
        button9 = "com.android.packageinstaller:id/virus_warning"
        button10 = "com.android.packageinstaller:id/done_button"
        button11 = "com.android.packageinstaller:id/continue_button"
        button_list = [button0, button1, button2, button3, button5, button6, button7, button4, button8, button9,
                       button10, button11]
        self.set_button_list(button_list)
        return super().element()


#



