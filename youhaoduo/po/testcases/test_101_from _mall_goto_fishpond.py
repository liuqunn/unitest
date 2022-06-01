import allure,time
from po.pages.base_page import BasePage
from po.driver.driver_YouHaoduo import DriverYouHaoduo
from selenium.webdriver.common.by import By
from po.pages.fishpond.fishpond_page import FishpondPage

@allure.feature('点击商城中https://www.tapd.cn/42524137/prong/stories/view/1142524137001000114?url_cache_key=from_url_story_list_2b309222bf625e80dd4e34c5bb5e9952&action_entry_type=story_tree_list')
class Test101:
    bt_receive = FishpondPage(BasePage)._bt_receive
    _save_img = 'test101.png'
    
    @allure.severity("critical")
    def setup_class(self):
        self.first = DriverYouHaoduo().first_start().first_page()

    def setup_method(self):
        pass
        
    @allure.story('从我的页面商城跳转鱼塘')
    def test_101(self):
        self.first.click_agree_btn()
        self.first.click_tv_pass()
        self.main = self.first.goto_mine()
        self.mall = self.main.goto_pointmall()
        self.mall.get_coin()
        if self.first.exists((By.ID,Test101().bt_receive)):
            assert self.first.shotscreen_find_text(self._save_img,'获得更多金币',(0,0.5,1,0.7))
        else:
            self.first.screenshot_crop(self._save_img,(0,0,1,1))
            assert False
        

    def teardown_method(self):
        pass

    def teardown_class(self):
        pass
