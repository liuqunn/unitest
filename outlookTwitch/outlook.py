from lib2to3.pgen2.driver import Driver
import re
import time,random
import webbrowser
from comm import Comm

class OutLook(Comm):
    outUrl = r"https://outlook.live.com/owa/"
    #登录相关
    singIn = "//a[@data-task= 'signin']"
    loginFmt = "//input[@name = 'loginfmt']"
    loginNextButton = "//div[@class = 'inline-block']"
    passWd = "//input[@name = 'passwd']"
    forgetPass = "//a[@id = 'idA_PWD_ForgotPassword']"
    
    #注册相关
    RegFreeAccount = "//div[@class = 'action']"
    
    MemberName = "//input[@id = 'MemberName']"
    PasswordInput = "//input[@id = 'PasswordInput']"
    NextButton1 = "//div[@class  = 'button-container']"
    
    LastName = "//input[@placeholder = '姓']"
    FirstName = "//input[@placeholder = '名']"
    NextButton2 = "//div[@class  = 'button-container no-margin-bottom']"
    
    BirthYear = "//input[@id = 'BirthYear']"     # 1905--2022之间
    BirthMonth = f"//option[@value = '{random.randint(1,12)}']"
    BirthDayDiv = "//div[@id = 'BirthDayContainer']"
    BirthDay = f"//select[@id = 'BirthDay']/option[@value = '{random.randint(1,28)}']"
    
    iframe1 = "//iframe[@id = 'enforcementFrame']"
    iframe2 = "//iframe[@id = 'fc-iframe-wrap']"
    iframe3 = "//iframe[@id = 'CaptchaFrame']"
    NextButton3 = "//button[@id = 'home_children_button']"
    
    Button = "//div[@class = 'col-xs-24 no-padding-left-right button-container']/div[1]"
    #邮箱内容相关
    #第一种情况
    reviceMsg = "//div[@title = '收件箱']"
    unread = "//div[@title = '收件箱']/span/span/span"
    msgInfo = "//div[@class = 'ZtMcNhhoIIOO6raJ3mUG']"
    #第二种情况
    unrd = "//span[@class = 'unrd']"
    refrash = "//a[@title = '收件箱']"
    mailInfo = "//h1[@class = 'bld']"
    
    def __init__(self,driver):
        self.driver = driver
        
    def login(self,mail,pwd):
        self.open_browser(self.outUrl)
        self.driver.find_element_by_xpath(self.singIn).click()
        self.driver.find_element_by_xpath(self.loginFmt).send_keys(mail)
        self.driver.find_element_by_xpath(self.loginNextButton).click()
        self.driver.find_element_by_xpath(self.passWd).send_keys(pwd)
        if self.judgEle(self.forgetPass):
            self.driver.find_element_by_xpath(self.loginNextButton).click()
            self.driver.find_element_by_xpath(self.Button).click()
        
    def regis(self,account,pwd,LName,FName):
        self.open_browser(self.outUrl)
        self.driver.find_element_by_xpath(self.RegFreeAccount).click()
        #邮箱名
        self.driver.find_element_by_xpath(self.MemberName).send_keys(account)
        self.driver.find_element_by_xpath(self.NextButton1).click()
        #密码
        self.driver.find_element_by_xpath(self.PasswordInput).send_keys(pwd)
        self.driver.find_element_by_xpath(self.NextButton1).click()
        #姓名
        self.driver.find_element_by_xpath(self.LastName).send_keys(LName)
        self.driver.find_element_by_xpath(self.FirstName).send_keys(FName)
        self.driver.find_element_by_xpath(self.NextButton2).click()
        #年月日
        self.driver.find_element_by_xpath(self.BirthYear).send_keys(random.randint(1960,1995))
        self.driver.find_element_by_xpath(self.BirthMonth).click()
        self.driver.find_element_by_xpath(self.BirthDayDiv).click()
        self.driver.find_element_by_xpath(self.BirthDay).click()
        self.driver.find_element_by_xpath(self.NextButton2).click()
        #机器人按钮
        # self.switch_frame(self.iframe1)
        # self.switch_frame(self.iframe2)
        # self.switch_frame(self.iframe3)
        # self.driver.find_element_by_xpath(self.NextButton3).click()
        # self.defult_frame()
        
        #图片验证码
        time.sleep(30)
        #保持登录状态
        self.driver.find_element_by_xpath(self.Button).click()
        return self.driver

    def msg_code(self):
        try:
            num1 = self.driver.find_element_by_xpath(self.unread).text
            for i in range(10):
                num2 = self.driver.find_element_by_xpath(self.unread).text
                if num2 > num1:
                    inbox = self.driver.find_element_by_xpath(self.msgInfo).get_attribute("aria-label")
                    return  re.search('[0-9]{6}',inbox).group()
                time.sleep(5)
        except:
            numBrackets = self.driver.find_element_by_xpath(self.unrd).text
            numnum = re.search('[0-9]',numBrackets).group()
            for i in range(10):
                self.driver.find_element_by_xpath(self.refrash).click()
                numBrackets = self.driver.find_element_by_xpath(self.unrd).text
                numnum1 = re.search('[0-9]',numBrackets).group()
                if numnum1 > numnum:
                    reciveMail = self.driver.find_element_by_xpath(self.mailInfo).text
                    return reciveMail.split(" ")[0]
                    # inbox = self.driver.find_element_by_xpath(self.msgInfo).get_attribute("aria-label")
                    # return  re.search('[0-9]{6}',inbox).group()
                time.sleep(5)
                
            
# if __name__ == "__main__":
#     outlook = OutLook()
#     # name1,pwd1 = ran_name_pw()
#     # Lname,Fname = ran_LName_FName()
#     # outlook.regis(name1,pwd1,Lname,Fname)
#     # inboxName = name1 + "@outlook.com"
#     # save_excel(inboxName,"outlook.xls")
#     outlook.login(read_excel("outlook.xls"),"Wwiuerhwoejrfoiwej")