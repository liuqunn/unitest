
# 1.在桌面浏览器图标属性--目标中添加 --remote-debugging-port=6001 
# 2.启动浏览器打开页面（保证只有一个浏览器打开）
# 3.运行脚本


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time,random
chrome_options = Options()
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:6001")
chrome_driver = r"C:\Users\liuqun\AppData\Local\Google\Chrome\Application"
driver = webdriver.Chrome(chrome_options=chrome_options)
for hand in driver.window_handles:
    driver.switch_to_window(hand)
    print(driver.title)
# print(driver.window_handles)
# for i in range(50):
#     try:
#         driver.find_element_by_xpath("//textarea[@data-a-target = 'chat-input']").send_keys(1)
#         driver.find_element_by_xpath("//button[@data-a-target = 'chat-send-button']").click()
#     except:
#         driver.find_element_by_xpath("//div[@data-a-target = 'chat-input']").send_keys(1)
#         driver.find_element_by_xpath("//button[@data-a-target = 'chat-send-button']").click()
#     time.sleep(1)
#     print(i)
