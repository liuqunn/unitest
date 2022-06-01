from selenium.webdriver.common.by import By
from po.pages.base_page import BasePage
import allure
from appium.webdriver.common.touch_action import TouchAction

class FishpondPage(BasePage):
    # 底部按钮
    _classify_page = 'com.xi.quickgame.mi:id/classify'
    _fishpond_page = 'com.xi.quickgame.mi:id/fish_pond'
    _discover_page = 'com.xi.quickgame.mi:id/discover'
    _recommend_page = 'com.xi.quickgame.mi:id/recommend'
    #领取金币按钮
    _bt_receive = 'com.xi.quickgame.mi:id/bt_receive'
    
    @allure.step('点击领取金币按钮')
    def click_bt_receive(self):
        self.find_id(self._bt_receive).click()