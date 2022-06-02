from twitchdriver import TwitchDriver

driver = TwitchDriver()
otlook = driver.outlok()
comm = driver.comm()
tch = driver.twit()
try:
    #注册邮箱
    name1,pwd1 = comm.ran_name_pw()
    Lname,Fname = comm.ran_LName_FName()
    otlook.regis(name1,pwd1,Lname,Fname)
    inboxName = name1 + "@outlook.com"

    #浏览器新建标签页
    comm.open_twitch()
    #切换标签页
    comm.switch_handle()
    #使用注册的邮箱注册twitch
    tch.twitch_regis(name1,pwd1,inboxName)
    comm.save_excel(inboxName,"outlook.xls")
except Exception as e:
    print(e)
    comm.close_chrome(0)
