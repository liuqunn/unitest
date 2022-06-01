
from datetime import datetime

from appium.webdriver.common.mobileby import MobileBy
from po.pages.base_page import BasePage
import allure


class SystemPage(BasePage):
    _notification = (MobileBy.XPATH, '//*[@text="通知"]')
    _notification_oc = (MobileBy.ID, 'android:id/switch_widget')


    @allure.step('点击通知')
    def click_notification(self):
        self.swipe_ratio(0.5, 0.6, 0.5, 0.4, 300)
        self.find(self._notification).click()
        self.sleep(2)


    @allure.step('点击通知开关')
    def click_notification_oc(self):
        eles = self.finds(self._notification_oc)
        eles[0].click()
        self.sleep(1)

    @allure.step('开关通知')
    def notification_oc(self):
        self.click_notification()
        self.click_tantan()
        self.click_notification_oc()


