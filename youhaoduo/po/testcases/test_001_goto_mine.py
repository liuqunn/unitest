import os
import time
import allure
from po.driver.driver_YouHaoduo import DriverYouHaoduo
from datetime import datetime
import pytest

@allure.feature('【ID1000101】打开app，进入我的页面')
#https://www.tapd.cn/42524137/prong/stories/view/1142524137001000101
class Test001:

    @allure.severity("critical")
    def setup_class(self):
        self.first = DriverYouHaoduo().first_start().first_page()

    def setup_method(self):
        pass

    @allure.story('进入我的页面')
    def test_01_goto_mine(self):
        self.first.click_agree_btn()
        self.first.sleep(2)
        self.mine = self.first.goto_mine()
        self.first.sleep(2)
        pic_name = r'{}.png'.format(time.time())
        now_pic = self.mine.screenshot_crop(pic_name,(0,0.5,1,0.6))
        assert self.first.compare_image(self.first.expected_pics + '/test_001.png', now_pic) > 0.999

    def teardown_method(self):
        pass

    def teardown_class(self):
        pass
