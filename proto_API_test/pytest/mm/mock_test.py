from glob import glob
import os
import os.path
import mock
from pytest_print import printer
import requests
import pytest
import allure


class UnixFS:

    @staticmethod
    def rm(filename):
        os.remove(filename)

    @staticmethod
    def ls(dir):
        return os.listdir(dir)


def abc():
    resp = requests.get(url="https://www.baidu.com")
    print("get resp.json() {}".format(resp.json()))
    return "abc"


def fake_json():
    return {"a": "bc"}


def response() -> requests.Response:
    ret = requests.Response
    ret.status_code = 200
    ret.text = "it's a test."
    ret.json = mock.Mock(return_value={"a": "bbb"})
    # ret.json = fake_json
    return ret


@pytest.mark.test01
def test_abc():
    # with mock.patch('mock_test.abc', return_value="mock abc"):
    #     assert abc() == "abc"
    with mock.patch('requests.get', return_value=response()):
        assert abc() == "abc", "值不相等抛出异常"

x = 100

@pytest.fixture
def a_change():
    global x
    print(x)
    x = 1
    print(x)
    return "  mysql_ConnPool   "

@allure.feature("测试样例1")
class TestExample:
    @pytest.mark.test02
    @pytest.mark.repeat(1)
    @allure.story("测试1")
    def test_fixture(a_change):
        print(x)

    @pytest.mark.test03
    @allure.story("测试2")
    def test_abc():
        # with mock.patch('mock_test.abc', return_value="mock abc"):
        #     assert abc() == "abc"
        with mock.patch('requests.get', return_value=response()):
            assert abc() == "abcc", "值不相等抛出异常"

if __name__ == "__main__":
    pytest.main(["-v", "-s", "--alluredir=./abc"])