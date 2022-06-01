from selenium.webdriver.common.by import By
from po.pages.base_page import BasePage
import allure
from appium.webdriver.common.touch_action import TouchAction




class RecommendPage(BasePage):
    #底部按钮
    _classify_page = 'com.xi.quickgame.mi:id/classify'
    _fishpond_page = 'com.xi.quickgame.mi:id/fish_pond'
    _discover_page = 'com.xi.quickgame.mi:id/discover'
    _recommend_page = 'com.xi.quickgame.mi:id/recommend'
    _mine_page = 'com.xi.quickgame.mi:id/mine'

    @allure.step('点击进入我的页面')
    def goto_mine(self):
        self.find_id(self._mine_page).click()
        return MinePage
