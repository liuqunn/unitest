from selenium import webdriver
from selenium.webdriver.chrome.options import Options
options = Options()
# 启动的浏览器地址
options.debugger_address ='127.0.0.1:8210'
# 将浏览器配置信息进行添加
driver = webdriver.Chrome(options=options)
print('目前浏览器标题：'+driver.title)