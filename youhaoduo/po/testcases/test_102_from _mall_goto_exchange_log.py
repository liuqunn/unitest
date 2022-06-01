import allure,time
from po.pages.base_page import BasePage
from po.driver.driver_YouHaoduo import DriverYouHaoduo
from selenium.webdriver.common.by import By
from po.pages.mine.mall_page import MallPage

@allure.feature('商城跳转兑换记录  https://www.tapd.cn/42524137/prong/stories/view/1142524137001000105?url_cache_key=from_url_story_list_2b309222bf625e80dd4e34c5bb5e9952&action_entry_type=story_tree_list')
class Test102:
    
    _save_img = 'test102.png'
    
    @allure.severity("critical")
    def setup_class(self):
        self.first = DriverYouHaoduo().first_start().first_page()

    def setup_method(self):
        pass
        
    @allure.story('商城跳转兑换记录')
    def test_102(self):
        self.first.click_agree_btn()
        self.first.click_tv_pass()
        self.main = self.first.goto_mine()
        self.mall = self.main.goto_pointmall()
        self.mall.exchange_log()
        if self.first.exists((By.XPATH,self.mall._page_title)):
            assert self.first.shotscreen_find_text(self._save_img,'兑换记录',(0,0.5,1,0.8))
        else:
            self.first.screenshot_crop(self._save_img,(0,0,1,1))
            assert False
        

    def teardown_method(self):
        pass

    def teardown_class(self):
        pass
