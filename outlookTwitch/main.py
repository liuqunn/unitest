from chromeDriver import chromeDriver
from comm import *

driver = chromeDriver()
otlook = driver.outlok()
tch = driver.twit()
#注册邮箱
name1,pwd1 = ran_name_pw()
Lname,Fname = ran_LName_FName()
otlook.regis(name1,pwd1,Lname,Fname)
inboxName = name1 + "@outlook.com"

#浏览器新建标签页
otlook.open_Js("https://www.twitch.tv/")

#使用注册的邮箱注册twitch
tch.twitch_regis(name1,pwd1,inboxName)
save_excel(inboxName,"outlook.xls")
