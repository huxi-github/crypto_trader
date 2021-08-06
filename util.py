# coding: utf-8

import datetime
import os
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL

from enum import Enum

# class LOG_LEVEL(Enum):
#     INFO = 0
#     DEGUG = 1
#     WARN = 2
#     ERROR = 3


def log(msg:str="kong msg"): #level:LOG_LEVEL=LOG_LEVEL.INFO,
    file = open("/Users/huxi/Desktop/altcoin_trend_rank.txt", "w+")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("[" + time + "]:\n" + msg)
    # print(msg)
    # file.write("[" + time + "][d]:"+ msg + "\n")
    file.close()

def warn(msg:str="kong warning msg"):
    file = open("altcoin_trend_rank.txt", "a+")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # print("[" + time + "]:" + msg)
    print(msg)
    file.write("[" + time + "][w]:"+ msg + "\n")
    file.close()

def send_email(mail_msg:str,mail_title:str='数字货币_活跃交易'):

    # qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    # sender_qq为发件人的qq号码
    sender_qq = '1324907549'
    # pwd为qq邮箱的授权码
    pwd = 'orxxpakxjfqkgdai'
    # 发件人的邮箱
    sender_qq_mail = '1324907549@qq.com'
    # 收件人邮箱
    receiver = 'huxi6615@gmail.com'
    # 邮件的正文内容
    mail_content = mail_msg
    # 邮件标题
    # mail_title = '数字货币_今日活跃交易'

    # ssl登录
    smtp = SMTP_SSL(host_server)
    # set_debuglevel()是用来调试的。参数值为1表示开启调试模式，参数值为0关闭调试模式
    smtp.set_debuglevel(1)
    smtp.ehlo(host_server)
    smtp.login(sender_qq, pwd)

    msg = MIMEText(mail_content, "plain", 'utf-8')
    msg["Subject"] = Header(mail_title, 'utf-8')
    msg["From"] = sender_qq_mail
    msg["To"] = receiver
    smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
    smtp.quit()

def check_and_update_msg(msg_id:str="kong msg",exc_name:str=""):
    # path = "new_msg_id_folder"
    path = "/Users/huxi/Desktop/new_msg_id_folder/"
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        log("初次部署,信息缓存文件"+path+'不存在')
        # 创建目录操作函数
        os.makedirs(path,mode=0x777,exist_ok=True)
        log("信息缓存文件夹"+ path + ' 创建成功')

    file = open(path+exc_name+"_new_msg_id.txt", "r+") #r+ 和w+ 都具有读写权限，w+在NULL会新创建新文件，原始内容抹除
    last_msg_id = file.readline()
    print("读取消息id" +last_msg_id)
    if last_msg_id != msg_id:
        file.seek(0,0)
        file.write(str(msg_id))
        file.close()
        return True
    else:
        return False

if __name__ == '__main__':
    send_email(" 尝试启动 交易对 BUSD_TLM ")

