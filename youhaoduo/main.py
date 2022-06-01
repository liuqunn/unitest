
import pytest

from po.driver.driver_YouHaoduo import DriverYouHaoduo
from po.pages.base_page import BasePage

if __name__ == '__main__':
    pytest.main(['./po/testcases/test_103_from_mine_goto_person_info.py','-v','-x','-s'])
    # pytest.main(['-v','-x','--alluredir ./report/allure'])
    # obj = DriverYouHaoduo().first_start()
    # obj.first_page().goto_fishpondpage()
    # BasePage(obj.driver).screenshot(r'D:\youhaoduo_appium\po\template_pics\test001.png')
    # BasePage(obj.driver).screenshot_crop(r'D:\youhaoduo_appium\po\template_pics\test001.png',(0,0.5,1,0.65))