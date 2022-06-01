from appium.webdriver.common.touch_action import TouchAction

from selenium.webdriver.common.by import By

from po.pages.base_page import BasePage



class MyGamePage(BasePage):
    #顶部按钮
    _back_btn = 'com.xi.quickgame.mi:id/left_back'
    _refresh_btn = (By.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout[2]/android.widget.TextView")
    _subscribe = (By.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout[3]/android.widget.TextView")
    _have=(By.XPATH,"/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout[1]/android.widget.FrameLayout[1]/android.widget.TextView")



    def click_refresh_btn(self):
        self.find(self._refresh_btn).click()

    def click_subscribe(self):
        self.find(self._subscribe).click()

    def click_have(self):
        self.find(self._have).click()