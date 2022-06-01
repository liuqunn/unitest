from selenium.webdriver.common.by import By
from po.pages.base_page import BasePage
import allure
from appium.webdriver.common.touch_action import TouchAction

class ClassifyPage(BasePage):
    #底部按钮
    _classify_page = 'com.xi.quickgame.mi:id/classify'
    _fishpond_page = 'com.xi.quickgame.mi:id/fish_pond'
    _discover_page = 'com.xi.quickgame.mi:id/discover'
    _recommend_page = 'com.xi.quickgame.mi:id/recommend'
