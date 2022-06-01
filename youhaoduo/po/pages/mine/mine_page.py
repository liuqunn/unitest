from po.pages.base_page import BasePage
import allure
from po.pages.mine.like_page import LikePage
from po.pages.mine.mall_page import MallPage
from po.pages.mine.mygame_page import MyGamePage
from po.pages.mine.settings_page import SettingsPage
from po.pages.mine.supplement_page import SupplementPage
from po.pages.mine.upload_page import UploadPage
from po.pages.mine.website_page import WebSitePage
from po.pages.mine.person_info import PersonInfo


class MinePage(BasePage):
    
    #列表页面入口
    _like = 'com.xi.quickgame.mi:id/rl_favorite'
    _pointsmall = 'com.xi.quickgame.mi:id/rl_points_mall'
    _mygame = 'com.xi.quickgame.mi:id/rl_my_game'
    _supplement = 'com.xi.quickgame.mi:id/rl_complement'
    _upload ='com.xi.quickgame.mi:id/rl_upload'
    _settings = 'com.xi.quickgame.mi:id/rl_setting'
    _website ='com.xi.quickgame.mi:id/tv_website'
    _qq_qun = 'com.xi.quickgame.mi:id/rl_qq_qun'
    _copy_btn = 'com.xi.quickgame.mi:id/copy'
    #头像
    _im_head =  'com.xi.quickgame.mi:id/im_head'
    #名字
    _tv_name = 'com.xi.quickgame.mi:id/tv_name'
    
    @allure.step('点击头像')
    def Im_Head(self):
        # self.sleep(1)
        self.find_id(self._im_head).click()
        return PersonInfo(self.driver)

    @allure.step('进入喜欢页面')
    def goto_like(self):
        # self.sleep(1)
        self.find_id(self._like).click()
        return LikePage(self.driver)

    @allure.step('进入积分商城')
    def goto_pointmall(self):
        # self.sleep(0.5)
        self.find_id(self._pointsmall).click()
        return MallPage(self.driver)

    @allure.step('进入游戏管理')
    def goto_mygame(self):
        self.find_id(self._mygame).click()
        return MyGamePage(self.driver)

    @allure.step('进入游戏补足')
    def goto_supplement(self):
        self.find_id(self._supplement).click()
        return SupplementPage(self.driver)

    @allure.step('进入上传短视频')
    def goto_upload(self):
        self.find_id(self._upload).click()
        return UploadPage(self.driver)

    @allure.step('进入设置')
    def goto_settings(self):
        self.find_id(self._settings).click()
        return SettingsPage(self.driver)

    @allure.step('进入官网')
    def goto_website(self):
        self.find_id(self._website).click()
        return WebSitePage(self.driver)

    @allure.step('点击qq群的复制')
    def copy_qq_number(self):
        self.swipe_ratio(0.4, 0.5, 0.8, 0.5)
        self.find_id(self._copy_btn).click()
        qqnumber = self.driver.getClipboardText()
        return qqnumber(self.driver)