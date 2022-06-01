import allure
import pytest
from po.driver.driver_YouHaoduo import DriverYouHaoduo

@allure.feature('打开个人信息页修改姓名为字母加汉字')
#https://www.tapd.cn/42524137/prong/stories/view/1142524137001000115?url_cache_key=from_url_story_list_2b309222bf625e80dd4e34c5bb5e9952&action_entry_type=story_tree_list
class Test103():

    _user_name = 'test测试'
    @allure.severity("critical")
    def setup_class(self):
        self.first = DriverYouHaoduo().first_start().first_page().goto_mine()

    def setup_method(self):
        pass
    @allure.story('进入设置页面修改玩家昵称')
    def test_103(self):
        self.person = self.first.Im_Head()
        self.person.find_id(self.person._et_name).send_keys(self._user_name)
        self.person.bt_save()
        user_name = self.first.find_id(self.first._tv_name).text
        assert user_name == self._user_name 