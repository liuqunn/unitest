import allure
from po.pages.base_page import BasePage



class MallPage(BasePage):
    #顶部返回按钮
    _back_btn = 'com.xi.quickgame.mi:id/left_back'
    #得金币按钮
    _get_coin = 'com.xi.quickgame.mi:id/iv_get_gold'
    #兑换记录按钮
    _exchange_log = 'com.xi.quickgame.mi:id/tv_exchange_log'
    #兑换记录页的标题
    _page_title = "//*[@text = '兑换记录']"
    
    
    @allure.step('点击得金币按钮')
    def get_coin(self):
        # self.sleep(1)
        self.find_id(self._get_coin).click()
        
    @allure.step('点击兑换记录按钮')
    def exchange_log(self):
        # self.sleep(1)
        self.find_id(self._exchange_log).click()