import random,time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from comm import *
from protoMail import ProtoMail

class Twitch(ProtoMail):
    
    loginButt = "//button[@data-a-target = 'login-button']"
    loginName = "//input[@aria-label = '请输入用户名']"
    loginPass = "//input[@aria-label = '输入密码']"
    loginComm = "//button[@data-a-target = 'passport-login-button']"
    
    copyMail = "//i[@class = 'mail icon copyable']"
    StarReg = "//button[@data-a-target = 'signup-button']"
    SignuserName = "//input[@aria-label = '创建一个用户名']"
    PassXpath = '//input[@class = "ScInputBase-sc-1wz0osy-0 ScInput-sc-m6vr9t-0 eUmSXX ewQTzt InjectLayout-sc-588ddc-0 hdZgVS tw-input tw-input--password"]' #1.密码  2.确认密码
    InputYear = '//input[@placeholder = "年"]'
    InputMonth = '//input[@aria-label = "请选择您的生日月份"]'
    MonthOpt = '//option[@value="5"]'
    InputDay = '//input[@placeholder = "日"]'
    UseMail = '//div[@class= "ScCoreButtonLabel-sc-lh1yxp-0 cbUefU"]'
    InputMail = '//input[@aria-label = "输入您的电子邮件地址"]'
    regisbut = "//button[@data-a-target = 'passport-signup-button']"  #完成注册按钮
    InputCode = "//input[@type = 'text']"   #验证码输入 
    codeXpth = "//tbody[@id = 'maillist']/tr/td[2]"
    seleTopic = "//button[@data-test-selector = 'onboarding-modal-splash-screen__button']" #选择话题按钮
    CloseButton = "//button[@data-a-target = 'modalClose']"   #关闭选择换题
    #机器人验证
    robb1 = "//button[@class = 'sc-bdnxRM DRUpX sc-kEqXSa']"
    # robb2 = f"//li[@id = 'image{random.randint(1,7)}']"
    
    searchInput = "//input[@aria-label = '搜索输入']"
    searchButt = "//button[@aria-label = '搜索按钮']"
    focus = "//div[@class = 'InjectLayout-sc-588ddc-0 gXJQci']"
    # focus = (By.XPATH,"//button[@aria-label = '关注']")
    sendMsg = "//textarea[@placeholder = '发送消息']"
    sendButton = "//button[@data-a-target = 'chat-send-button']"
        
    def find_ele(self,local):
        time.sleep(round(random.uniform(0,1),1))
        return  WebDriverWait(self.driver,120,0.5).until(EC.visibility_of_element_located(local))
    
    def find_eles(self,local):
        time.sleep(round(random.uniform(0,1),1))
        WebDriverWait(self.driver,60,0.5).until(EC.visibility_of_element_located(local))
        return self.driver.find_elements(*local)
    
    def twitch_login(self,username,passwd):
        self.driver.get("https://www.twitch.tv/")
        WebDriverWait(self.driver,60,0.5).until(EC.visibility_of_element_located((By.XPATH,self.loginButt))).click()
        WebDriverWait(self.driver,60,0.5).until(EC.visibility_of_element_located((By.XPATH,self.loginName))).send_keys(username)
        WebDriverWait(self.driver,60,0.5).until(EC.visibility_of_element_located((By.XPATH,self.loginPass))).send_keys(passwd)
        WebDriverWait(self.driver,60,0.5).until(EC.visibility_of_element_located((By.XPATH,self.loginComm))).click()
    
    def twitch_regis(self,twitch_name,passd,protoMail):
        # self.driver.get("https://www.twitch.tv/")
        time.sleep(round(random.uniform(0,2),1))
        self.driver.find_element_by_xpath(self.StarReg).click()
        self.driver.find_element_by_xpath(self.SignuserName).send_keys(twitch_name)
        PassXpath = self.driver.find_elements_by_xpath(self.PassXpath)
        for i in PassXpath:
            i.send_keys(passd)
        self.driver.find_element_by_xpath(self.InputYear).send_keys(random.randint(1990,1995))
        self.driver.find_element_by_xpath(self.MonthOpt).click()
        self.driver.find_element_by_xpath(self.InputDay).send_keys(random.randint(1,27))
        self.driver.find_element_by_xpath(self.UseMail).click()
        self.driver.find_element_by_xpath(self.InputMail).send_keys(protoMail)
        WebDriverWait(self.driver,60).until(EC.element_to_be_clickable((By.XPATH,self.regisbut)))
        time.sleep(round(random.uniform(1,2),1))
        self.driver.find_element_by_xpath(self.regisbut).click()
        
    
    def Input_code(self,VeryCode):
        self.driver.find_element_by_xpath(self.InputCode).send_keys(VeryCode)
    
    #关闭登录完成之后的弹窗    
    def set_topic(self):  
        WebDriverWait(self.driver,60).until(EC.visibility_of_element_located((By.XPATH,self.seleTopic)))
        self.driver.find_element_by_xpath(self.seleTopic).click()
        time.sleep(round())
        self.driver.find_element_by_xpath(self.CloseButton).click()
        
    def select_topic(self):
        WebDriverWait(self.driver,60).until(EC.visibility_of_element_located((By.XPATH,self.seleTopic)))
        self.driver.find_element_by_xpath(self.seleTopic).click()
        time.sleep(round(random.uniform(0,1),1))
        self.driver.find_element_by_xpath(self.CloseButton).click()
        
    def subCreat(self,HostName):
        #HostName主播名字    #fensi  粉丝名字
        self.driver.find_element_by_xpath(self.searchInput).send_keys(HostName)
        self.driver.find_element_by_xpath(self.searchButt).click()
        self.driver.find_element_by_xpath(r"//a[@href = '%s']"%(HostName)).click()
        time.sleep(2)
        self.find_ele(self.focus).click()
        ranName = random.sample('1ASDzQyx2wvu3tFGHJsr4Wqpo5EnZXCmKLJ6lkRj7iThg8feYd9MNBVUIOPcba0',random.randint(3,9))
        ranName1 = "".join(ranName)
        self.find_ele(self.sendMsg).send_keys("%s coming"%ranName1)
        self.driver.find_element_by_xpath(self.sendButton).click() 
        
        
