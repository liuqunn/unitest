from selenium.webdriver.common.by import By
from po.pages.base_page import BasePage
import allure
from appium.webdriver.common.touch_action import TouchAction





class LikePage(BasePage):
    # title
    _like_title = 'com.xi.quickgame.mi:id/tv_title'
    _short_video =(By.XPATH, "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.LinearLayout[1]/android.widget.TextView[2]")
    _subject = (By.XPATH, "//*[@text='专题']")



    def click_subject(self):
        self.find(self._subject).click()


    def click_short_video(self):
        self.find(self._short_video).click()