import random,time
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Twitch():
    
    #tempmail
    tempMail = "//input[@id = 'fe_text']"   #没有临时邮箱的时候没有value属性
    tempCode = "//tr/td[2]/a[@class = 'row-link']"
    
    #twitch
    loginButt = "//button[@data-a-target = 'login-button']"
    loginName = "//input[@aria-label = '请输入用户名']"
    loginPass = "//input[@aria-label = '输入密码']"
    loginComm = "//button[@data-a-target = 'passport-login-button']"
    StarReg = "//button[@data-a-target = 'signup-button']"
    SignuserName = "//input[@aria-label = '创建一个用户名']"
    CreatPass = "//input[@aria-label = '创建一个安全密码']"
    PassXpath = '//input[@autocomplete = "current-password"]' #1.密码  2.确认密码
    # PassXpath = '//input[@class = "ScInputBase-sc-1wz0osy-0 ScInput-sc-m6vr9t-0 JSHTV jZksOX InjectLayout-sc-588ddc-0 cofvtY tw-input tw-input--password"]' #1.密码  2.确认密码
    InputYear = '//input[@placeholder = "年"]'
    InputMonth = '//input[@aria-label = "请选择您的生日月份"]'
    MonthOpt = '//option[@value="5"]'
    InputDay = '//input[@placeholder = "日"]'
    UseMail = '//div[@class= "Layout-sc-nxg1ff-0 eMBxHr"]'
    InputMail = '//input[@aria-label = "输入您的电子邮件地址"]'
    regisbut = "//button[@data-a-target = 'passport-signup-button']"  #完成注册按钮
    # InputCode = "//input[@type = 'text']"   #验证码输入 
    InputCode = "//input[@inputmode = 'numeric']"   #验证码输入 
    seleTopic = "//button[@data-test-selector = 'onboarding-modal-splash-screen__button']" #选择话题按钮
    CloseButton = "//button[@data-a-target = 'modalClose']"   #关闭选择换题
    #机器人验证
    robb1 = "//button[@class = 'sc-bdnxRM DRUpX sc-kEqXSa']"
    # robb2 = f"//li[@id = 'image{random.randint(1,7)}']"
    
    searchInput = "//input[@aria-label = '搜索输入']"
    searchButt = "//button[@aria-label = '搜索按钮']"
    # focus = (By.XPATH,"//div[@class = 'InjectLayout-sc-588ddc-0 gXJQci']")
    focus = (By.XPATH,"//button[@aria-label = '关注']")
    # focus = (By.XPATH,"//div[@class = 'InjectLayout-sc-588ddc-0 bupOpr']")
    
    IKnow = "//p[@class = 'CoreText-sc-cpl358-0 onWG']"
    sendMsg = (By.XPATH,"//div[@data-slate-node = 'element']")
    sendButton = "//button[@data-a-target = 'chat-send-button']"
    
    def __init__(self):
        # 进入浏览器设置
        options = Options()
        #解决报错 returned -1, SSL error code 1, net_error -100
        options.add_argument('--ignore-certificate-errors') 
        options.add_argument('--ignore-ssl-errors')
        options.add_experimental_option('excludeSwitches',['enable-automation'])
        
        #添加代理
        # proxy_arr = [
        #     '--proxy-server=https://116.163.46.231:10091',
        #     '--proxy-server=https://146.56.110.131:1443',
        #     '--proxy-server=https://193.110.203.34:1443', 
        #     '--proxy-server=https://103.117.103.120:443',  
        #     '--proxy-server=https://183.232.56.110:10094' 
        #     ]
        # proxy = random.choice(proxy_arr)  # 随机选择一个代理
        # print(proxy) #如果某个代理访问失败,可从proxy_arr中去除
        # options.add_argument(proxy)  # 添加代理
        
        #随机请求头
        options.add_argument('--disable-gpu')
        user_agent = UserAgent().chrome
        options.add_argument('user-agent=%s'%user_agent)
        
        # # 创建浏览器对象
        self.driver = webdriver.Chrome(options=options)
        self.driver.implicitly_wait(120)
    
    def open_lable(self):
        js = 'window.open("https://www.twitch.tv/");'
        self.driver.execute_script(js)
    
    def jump_judge(self,local):
        try:
            WebDriverWait(self.driver,30,0.5).until(EC.visibility_of_element_located(local))
            return True
        except:
            return False
        
    def Twitch_jump_judge(self,local):
        try:
            WebDriverWait(self.driver,30,0.5).until(EC.visibility_of_element_located((By.XPATH,local)))
            return True
        except:
            return False
    
    def find_ele(self,local):
        time.sleep(round(random.uniform(0,1),1))
        return  WebDriverWait(self.driver,90,0.5).until(EC.visibility_of_element_located(local))
    
    def switch_handle(self):
        # 对窗口进行遍历
        handle = self.driver.current_window_handle
        handles = self.driver.window_handles
        for newhandle in handles:
            # 筛选新打开的窗口B
            if newhandle!=handle:
                # 切换到新打开的窗口B
                self.driver.switch_to.window(newhandle)
        
    def temp_mail(self):
        self.driver.get("https://10minutemail.net")
        time.sleep(1.5)
        for i in range(5):
            try:
                mail = self.driver.find_element_by_xpath(self.tempMail).get_attribute("value")
                if mail=="":
                    continue
                else:
                    break
            except:
                time.sleep(1)
                pass
        return mail
            
    def twitch_regis(self,twitch_name,passd,protoMail):
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
        while True:
            if self.Twitch_jump_judge(self.InputCode):
                break
            else:
                try:
                    self.driver.find_element_by_xpath(self.regisbut).click()
                except:
                    break
    def get_code(self):
        for i in range(30):
            try:
                codeMsg = self.driver.find_element_by_xpath(self.tempCode).text
                code = codeMsg.split(" ")[0]
                print(type(code))
                if len(code) == 6:
                    return code
                time.sleep(5)
            except:
                time.sleep(2)
        
    
    def Input_code(self,VeryCode):
        self.driver.find_element_by_xpath(self.InputCode).send_keys(VeryCode)
    
    #关闭登录完成之后的弹窗
    def select_topic(self):
        # WebDriverWait(self.driver,60).until(EC.visibility_of_element_located((By.XPATH,self.seleTopic)))
        self.driver.find_element_by_xpath(self.seleTopic).click()
        time.sleep(round(random.uniform(0,1),1))
        self.driver.find_element_by_xpath(self.CloseButton).click()
        
    def subCreat(self,HostName):
        #HostName主播名字    #fensi  粉丝名字
        self.driver.find_element_by_xpath(self.searchInput).send_keys(HostName)
        self.driver.find_element_by_xpath(self.searchButt).click()
        self.driver.find_element_by_xpath("//a[@href = '/%s']"%(HostName)).click()
        time.sleep(5)
        self.find_ele(self.focus).click()
        ranName = random.sample('1ASDzQyx2wvu3tFGHJsr4Wqpo5EnZXCmKLJ6lkRj7iThg8feYd9MNBVUIOPcba0',random.randint(13,19))
        ranName1 = "".join(ranName)
        self.find_ele(self.sendMsg).send_keys("%s coming"%ranName1)
        self.find_ele(self.sendMsg).send_keys("%s coming"%ranName1)
        time.sleep(1)
        self.driver.find_element_by_xpath(self.sendButton).click() 

    def close_chrome(self,min):
        # time.sleep(15)
        # self.driver.minimize_window()
        time.sleep(min*60)
        self.driver.quit()
        
    def tempMail_regis_twitch(self,authers):
        passd = "qwiuerhwoejrfoiwej"
        ranName = random.sample('1ASDzQyx2wvu3tFGHJsr4Wqpo5EnZXCmKLJ6lkRj7iThg8feYd9MNBVUIOPcba0',random.randint(20,25))
        ranMail = self.temp_mail()
        self.open_lable()
        self.switch_handle()
        self.twitch_regis("".join(ranName),passd,ranMail) 
        self.switch_handle()
        getCode = self.get_code()
        self.switch_handle()
        self.Input_code(getCode)
        self.select_topic()
        for auther in authers:
            try:
                self.subCreat(auther)
                time.sleep(3)
            except:
                pass
        
if __name__ == '__main__':
    twitch = Twitch()
    twitch.tempMail_regis_twitch(["soifjsdgijerro"])
    # twitch.tempMail_regis_twitch(["luckysaki","watch10kt","miles_zhang","wang2dade","skylee83","hadeslee9","wz0823","kinggo_shang","simon_4812","qinliping","mozun_x"])
    # twitch.close_chrome(0)