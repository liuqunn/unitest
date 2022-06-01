import time,random,os,threading
from matplotlib.pyplot import magma
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support  import expected_conditions as EC
from comm import *
import xlrd as xr
from fake_useragent import UserAgent
from outlook import OutLook
from twitch import Twitch


class chromeDriver:
    def __init__(self):
        # 进入浏览器设置
        options = webdriver.ChromeOptions()
        #解决报错 returned -1, SSL error code 1, net_error -100
        options.add_argument('--ignore-certificate-errors') 
        options.add_argument('--ignore-ssl-errors')
        options.add_experimental_option('excludeSwitches',['enable-automation'])
        
        #随机请求头
        options.add_argument('--disable-gpu')
        user_agent = UserAgent().chrome
        options.add_argument('user-agent=%s'%user_agent)
        
        # # 创建浏览器对象
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(120)
    
    def open_Js(self,url):
        js = f'window.open({url});'
        self.driver.execute_script(js)
        
    def open_browser(self,url):
        self.driver.get(url)
    
    def switch_handle(self):
        # 对窗口进行遍历
        handle = self.driver.current_window_handle
        handles = self.driver.window_handles
        for newhandle in handles:
            # 筛选新打开的窗口B
            if newhandle!=handle:
                # 切换到新打开的窗口B
                self.driver.switch_to.window(newhandle)
                
            
    def close_chrome(self,min):
        time.sleep(15)
        self.driver.minimize_window()
        time.sleep(min*60)
        self.driver.quit()
        
    #切换到指定frame
    def switch_frame(self,fram_xpath):
        # WebDriverWait(self.driver,120,0.5).until(EC.frame_to_be_available_and_switch_to_it(fram_xpath))
        self.driver.switch_to_frame(fram_xpath)
        
    #切换到默认的frame
    def defult_frame(self):
        self.driver.switch_to.default_content()
        
    def judgEle(self,eleXpath):
        try:
            WebDriverWait(self.driver,20).until(EC.invisibility_of_element_located((By.XPATH,eleXpath)))
            return True
        except:
            return False
        
    def read_excel(filenname):
        excelMails = []
        file_path = os.path.dirname(__file__)
        file = file_path + '\\' + filenname
        oldwb = xr.open_workbook(file)#打开工作簿
        sheet = oldwb.sheets()[0]
        for i in range(sheet.nrows):
            excelMails.append(sheet.cell_value(i,0))
        return excelMails
    
    def save_excel(mailAD,filenname):
        file_path = os.path.dirname(__file__)
        file = file_path + '\\' + filenname
        oldwb = xr.open_workbook(file)#打开工作簿
        sheet = oldwb.sheets()[0]
        # print(sheet.nrows)
        newwb = copy.copy(oldwb)#复制出一份新工作簿
        newws = newwb.get_sheet(0)#获取指定工作表，0表示实际第一张工作表
        # for i in range(len(mailAD)):
            # line_count = 
        # newws.write(int(i+int(sheet.nrows)), 0, mailAD[i]) #把列表a中的元素逐个写入第一列，0表示实际第1列,i+1表示实际第i+2行
        newws.write(int(sheet.nrows), 0, mailAD) #把列表a中的元素逐个写入第一列，0表示实际第1列,i+1表示实际第i+2行
            # print("行数为 ：" + str(i+int(sheet.nrows)))
        newwb.save(file)#保存修

    def ran_name_pw():
        passd = "Wwiuerhwoejrfoiwej"
        ranName = random.sample('ASDzQyxwvutFGHJsrWqpoEnZXCmKLJlkRjiThgfeYdMNBVUIOPcba',random.randint(20,25))
        ranMail = "".join(ranName)
        return ranMail,passd

    def ran_LName_FName():
        qwer = random.sample('1ASDzQyx2wvu3tFGHJsr4Wqpo5EnZXCmKLJ6lkRj7iThg8feYd9MNBVUIOPcba0',random.randint(1,5))
        qwe = random.sample('1ASDzQyx2wvu3tFGHJsr4Wqpo5EnZXCmKLJ6lkRj7iThg8feYd9MNBVUIOPcba0',random.randint(1,5))
        return qwer,qwe
    
    def open_Js(self,url):
        js = f'window.open({url});'
        self.driver.execute_script(js)
        
    def ele_click(self,ele):
        self.driver.find_element_by_xpath(ele).click()
    
    def ele_sendKeys(self,ele,msg):
        self.driver.find_element_by_xpath(ele).send_keys(msg)
    
        
        
    def outlok(self):
        return OutLook(self)
    
    def twit(self):
        return Twitch(self)