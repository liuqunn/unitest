# import requests
# import mock

# def get_id()->int:
#     return 10

# # def test_get_id():
# #     assert get_id() == 11



# def abc()->int:
#     resp = requests.get(url="https://devapi.ckmile.cn")
#     print("get resp.json() {}".format(resp.json()))
#     return resp

# def abc2()->int:
#     resp = requests.get(url="https://www.baidu.com")
#     print("get resp.json() {}".format(resp.text))
#     return resp

# def m_json():
#     return {"a":"b"}

# def m_resp()->requests.Response:
#     ret = requests.Response
#     ret.status_code = 200
#     ret.text = "it's a test."
#     ret.json = m_json
#     return ret




# def multi():
#     return abc()

# def multi2():
#     return abc2()


# def test_abc():
#     with mock.patch('example.multi', return_value=m_resp):
#         assert abc().status_code == 404, "值不相等抛出异常"
#     assert abc2().status_code == 200

# def test_abcdef():
#     with mock.patch('example.multi', return_value=m_resp):
#         assert abc().status_code == 404, "值不相等抛出异常"
#     assert abc2().status_code == 200



import mock

def dfj()->int:
    return add2(1,2)


def add2(x,y):
    return x+y


def add1():
    result1 = mock.Mock(return_value = "9183467892347")
    
    add2 = result1
    print(dfj())


add1()
