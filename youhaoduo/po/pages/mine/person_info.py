from msilib.schema import Class
from po.pages.base_page import BasePage
import allure


class PersonInfo(BasePage):
    #顶部返回按钮
    _left_back = 'com.xi.quickgame.mi:id/alivc_base_iv_left_back'
    #保存按钮
    _bt_save = 'com.xi.quickgame.mi:id/bt_save'
    #头像
    _head = 'com.xi.quickgame.mi:id/head'
    #昵称
    _et_name = 'com.xi.quickgame.mi:id/et_name'
    #生日
    _et_age = 'com.xi.quickgame.mi:id/et_age'
    #性别 无
    _rb_no = 'com.xi.quickgame.mi:id/rb_no'
    #性别男
    _rb_man = 'com.xi.quickgame.mi:id/rb_man'
    #性别女
    _rb_woman ='com.xi.quickgame.mi:id/rb_woman'
    #个人签名
    _et_signature = 'com.xi.quickgame.mi:id/et_signature'
    #喜好游戏单选框  resource-id
    _cb_like = 'com.xi.quickgame.mi:id/cb_like'
    
    @allure.step('点击保存按钮')
    def bt_save(self):
        self.find_id(self._bt_save).click()
    
    
    