import os
import time
import  allure
from po.driver.driver_YouHaoduo import DriverYouHaoduo
from datetime import datetime
import pytest

@allure.feature('【ID1000110】游戏管理页面各子tab间可以互相切换')
#https://www.tapd.cn/42524137/prong/stories/view/1142524137001000110
class Test001:

    @allure.severity("critical")
    def setup_class(self):
        self.first = DriverYouHaoduo().first_start().first_page()
        self.first.click_agree_btn()
        self.first.sleep(2)
        self.mygame = self.first.goto_mine().goto_mygame()

    def setup_method(self):
        pass

    @allure.story('点击更新')
    def test_05_click_refresh(self):
        self.mygame.click_refresh_btn()
        self.first.sleep(2)
        pic_name_05 = r'{}.png'.format(time.time())
        now_pic = self.mygame.screenshot_crop(pic_name_05, (0, 0.02, 1, 0.16))
        assert self.first.compare_image(self.first.expected_pics + '/test_005_01.png', now_pic) > 0.999

    @allure.story('点击预约')
    def test_06_click_subscribe(self):
        self.mygame.click_subscribe()
        self.first.sleep(2)
        pic_name_06 = r'{}.png'.format(time.time())
        now_pic = self.mygame.screenshot_crop(pic_name_06, (0, 0.02, 1, 0.16))
        assert self.first.compare_image(self.first.expected_pics + '/test_005_02.png', now_pic) > 0.999

    def teardown_method(self):
        pass

    def teardown_class(self):
        pass
