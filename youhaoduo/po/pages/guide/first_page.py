from po.pages.base_page import BasePage
import allure
from po.pages.classify.classify_page import ClassifyPage
from po.pages.discover.discover_page import DiscoverPage
from po.pages.fishpond.fishpond_page import FishpondPage
from po.pages.recommend.recommend_page import RecommendPage
from po.pages.base_page import BasePage
from po.pages.mine.mine_page import MinePage
from po.pages.recommend.recommend_page import RecommendPage


class FirstPage(BasePage):
    '''
    欢迎页
    '''
    #同意进入app
    _agree_btn = 'com.xi.quickgame.mi:id/tv_agree'
    #不同意
    _disagree_btn = 'com.xi.quickgame.mi:id/tv_disagree'
    
    #必玩弹窗一键加载
    _tv_go = 'com.xi.quickgame.mi:id/tv_go'
    #必玩弹窗遗憾错过
    _tv_pass = 'com.xi.quickgame.mi:id/tv_pass'
    
    #系统弹窗 允许
    _allow_btn = 'com.android.packageinstaller:id/permission_allow_button'
    #系统弹窗 拒绝
    _deny_btn = 'com.android.packageinstaller:id/permission_deny_button'

    # 底部按钮
    _classify_page = 'com.xi.quickgame.mi:id/classify'
    _fishpond_page = 'com.xi.quickgame.mi:id/fish_pond'
    _discover_page = 'com.xi.quickgame.mi:id/discover'
    _recommend_page = 'com.xi.quickgame.mi:id/recommend'
    _mine_page = 'com.xi.quickgame.mi:id/mine'

    @allure.step('点击同意进入软件')
    def click_agree_btn(self):
        self.find_id(self._agree_btn).click()
        
    @allure.step('点击不同意退出软件')
    def click_disagree_btn(self):
        self.find_id(self._disagree_btn).click()
        
    @allure.step('点击系统弹窗允许')
    def click_deny_btn(self):
        self.find_id(self._deny_btn).click()
        
    @allure.step('点击系统弹窗拒绝')
    def click_allow_btn(self):
        self.find_id(self._allow_btn).click()
        
    @allure.step('点击必玩弹窗遗憾错过')
    def click_tv_pass(self):
        self.find_id(self._tv_pass).click()
        
    @allure.step('必玩弹窗一键加载')
    def click_tv_go(self):
        self.find_id(self._tv_go).click()

    @allure.step('进入发现页面')
    def goto_fishpondpage(self):
        # self.sleep(1)
        self.find_id(self._discover_page).click()
        # self.sleep(1)
        return DiscoverPage(self.driver)

    @allure.step('进入分类页面')
    def goto_classifypage(self):
        # self.sleep(1)
        self.find_id(self._classify_page).click()
        # self.sleep(1)
        return ClassifyPage(self.driver)

    @allure.step('进入招财页面')
    def goto_fishpondpage(self):
        # self.sleep(1)
        self.find_id(self._fishpond_page).click()
        # self.sleep(1)
        return FishpondPage(self.driver)

    @allure.step('进入推荐页面')
    def goto_recommendpage(self):
        # self.sleep(1)
        self.find_id(self._recommend_page).click()
        # self.sleep(1)
        return RecommendPage(self.driver)

    @allure.step('点击进入我的页面')
    def goto_mine(self):
        self.find_id(self._mine_page).click()
        return MinePage(self.driver)


