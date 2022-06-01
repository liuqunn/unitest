from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.common.by import By

from po.pages.base_page import BasePage



class UploadPage(BasePage):
    #顶部按钮
    _back_btn = 'com.xi.quickgame.mi:id/left_back'