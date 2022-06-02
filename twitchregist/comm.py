import os,random
import xlrd as xr
from xlutils import copy

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