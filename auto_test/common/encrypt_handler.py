import time
import base64

import rsa


def rsa_encrypt(msg: str, pub_key: str):
    """
    公钥加密
    :param msg: 要加密的内容 str
    :param pub_key: pem格式的公钥字符串
    :return:
    """
    # 1. 生成公钥对象
    # 把公钥字符串转换为字节数据
    pub_key_bytes = pub_key.encode()
    pub = rsa.PublicKey.load_pkcs1_openssl_pem(pub_key_bytes)
    # 待加密的数据转换为字节数据
    content = msg.encode('utf-8')
    # 2. 加密
    crypt_msg = rsa.encrypt(content, pub)
    # 3. 转换成base64字符串返回
    return base64.b64encode(crypt_msg).decode()


def generate_sign(token, pub_key):
    """
    生成签名
    :param token: token字符串
    :param pub_key: pem格式的公钥
    :return:
    """
    # 1.获取token的前50位
    token_50 = token[:50]
    # 获取timestamp
    timestamp = int(time.time())
    # 拼接token的前50位 和时间戳
    msg = token_50 + str(timestamp)

    # 进行RSA加密
    sign = rsa_encrypt(msg, pub_key)
    return sign, timestamp


if __name__ == '__main__':
    import requests
    import settings
    from common.fixture import register, login
    from common.test_data_handler import generate_no_use_phone
    mobile_phone = generate_no_use_phone()
    pwd = '123456678'
    if not register(mobile_phone, pwd):
        raise ValueError('注册错误')

    res = login(mobile_phone, pwd)
    if not res:
        raise ValueError('登录失败')

    token = res['token_info']['token']
    sign, timestamp = generate_sign(token, settings.SERVER_RSA_PUB_KEY)
    headers = {
        "X-Lemonban-Media-Type": "lemonban.v3",
        "Authorization": "Bearer "+token
    }
    data = {
        'member_id': res['id'],
        'amount': 5000,
        'timestamp': timestamp,
        'sign': sign
    }
    url = settings.PROJECT_HOST + settings.INTERFACES['recharge']
    response = requests.post(url=url, json=data, headers=headers)
    print(response.status_code)
    print(response.json())
