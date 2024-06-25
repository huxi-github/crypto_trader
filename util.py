# coding: utf-8
import math

from playsound import playsound
import datetime
import os
from pathlib import Path
import sys
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
# 语音播报模块
import pyttsx3
import numpy as np

from enum import Enum
import re

# class LOG_LEVEL(Enum):
#     INFO = 0
#     DEGUG = 1
#     WARN = 2
#     ERROR = 3


def log(msg:str="kong msg"): #level:LOG_LEVEL=LOG_LEVEL.INFO,
    path = "log/"
    if sys.platform=='linux':
        path = "/root/"
    path_log = Path(path+"altcoin_trend_rank.txt")
    if not path_log.exists():
        print("第一次执行，创建日志文件..")
        file = open(path+"altcoin_trend_rank.txt", "a+") #1.没有则创建 2.追加写入
    else:
        file = open(path + "altcoin_trend_rank.txt", "a")  # 1.读写,追加
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("[" + time + "]:\n" + msg)
    # print(msg)
    # file.write("[" + time + "][d]:"+ msg + "\n") #暂时不用这个文件
    file.close()

#//记录日志,指定文件
def log_to_file(msg:str="kong msg",file_name:str="aaa"):
    pre_path = "log"
    if sys.platform=='linux':
        pre_path = "/root"
    log_f_path = pre_path+'/'+file_name #全路径
    if not os.path.exists(log_f_path):
        print("新文件,创建"+log_f_path)
        file = open(log_f_path, "a+") #1.没有则创建 2.追加写入
    else:
        file = open(log_f_path, "a")  # 1.读写,追加
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("写入日志[" + time + "]:\n" + msg)
    file.write("[" + time + "][I]:"+ msg + "\n") #暂此方法需要写入文件
    file.close()

def warn(msg:str="kong warning msg"):
    file = open("altcoin_trend_rank.txt", "a+")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # print("[" + time + "]:" + msg)
    print(msg)
    file.write("[" + time + "][w]:"+ msg + "\n")
    file.close()

def read_log_file_last_profit_count(file_name:str=""):
    pre_path = "log"
    if sys.platform=='linux':
        pre_path = "/root"
    log_f_path = pre_path+'/'+file_name #全路径
    if not os.path.exists(log_f_path):
        print("文件不存在.."+log_f_path)
    else:
        file = open(log_f_path, "r")  # 1.读写,追加
    print("读取日志:")
    lines = file.readlines()[-800:]    # 接收数据
    zhiying_count=0
    zhisun_count=0
    date_today = datetime.datetime.now().strftime("%Y-%m-%d ")
    date_today_1 = (datetime.date.today() + datetime.timedelta(-1)).strftime("%Y-%m-%d ")
    for line in lines:
        if date_today in line :
            # print(line)
            matchObj = re.search( r'.*BUSD止盈.*', line)
            if matchObj:
                zhiying_count+=1
                print("match --> : ", matchObj.group())
        if date_today_1 in line :
            # print(line)
            matchObj = re.search( r'.*BUSD止盈.*', line)
            if matchObj:
                zhiying_count+=1
                print("match --> : ", matchObj.group())
        if date_today in line :
            # print(line)
            matchObj = re.search( r'.*BUSD止损.*', line)
            if matchObj:
                zhisun_count+=1
                print("match --> : ", matchObj.group())

    profit_sum=zhiying_count-2*zhisun_count
    print("昨今止盈数"+str(zhiying_count))
    print("昨今止损数"+str(zhisun_count))
    print("昨今盈利数"+str(profit_sum))
    return profit_sum

# def parse_log_file_last_profit_count(file_name:str=""):
#     pre_path = "log"
#     if sys.platform=='linux':
#         pre_path = "/root"
#     log_f_path = pre_path+'/'+file_name #全路径
#     if not os.path.exists(log_f_path):
#         print("文件不存在.."+log_f_path)
#     else:
#         file = open(log_f_path, "r")  # 1.读写,追加
#     print("读取日志:")
#     lines = file.readlines()    # 接收数据

#     for day_delta in range(40):
#         zhiying_count=0
#         zhisun_count=0
#         date_today = (datetime.datetime.now() + datetime.timedelta(-day_delta)).strftime("%Y-%m-%d ")
#         date_today_1 = (datetime.date.today() + datetime.timedelta(-1) + datetime.timedelta(-day_delta)).strftime("%Y-%m-%d ")
#         for line in lines:
#             if date_today in line :
#                 # print(line)
#                 matchObj = re.search( r'.*BUSD止盈.*', line)
#                 if matchObj:
#                     zhiying_count+=1
#                     # print("match --> : ", matchObj.group())
#             if date_today_1 in line :
#                 # print(line)
#                 matchObj = re.search( r'.*BUSD止盈.*', line)
#                 if matchObj:
#                     zhiying_count+=1
#                     # print("match --> : ", matchObj.group())
            

#             if date_today in line :
#                 # print(line)
#                 matchObj = re.search( r'.*BUSD止损.*', line)
#                 if matchObj:
#                     zhisun_count+=1
#                     # print("match --> : ", matchObj.group())
#         print(date_today)
#         print("今昨止盈数"+str(zhiying_count))
#         print("今日止损数"+str(zhisun_count))
#         print()
#         return

def simu_test(file_name:str="",stop_profit_count=1):
    pre_path = "log"
    if sys.platform=='linux':
        pre_path = "/root"
    log_f_path = pre_path+'/'+file_name #全路径
    if not os.path.exists(log_f_path):
        print("文件不存在.."+log_f_path)
    else:
        file = open(log_f_path, "r")  # 1.读写,追加
    print("读取日志:")
    lines = file.readlines()    # 接收数据

    profit_sum = 0
    tot_zhisun =0
    x = []
    y = []
    z = []
    s = []
    ss= []
    for day_delta in range(-50,0):
        zhiying_count=0
        zhisun_count=0
        date_today = (datetime.datetime.now() + datetime.timedelta(day_delta)).strftime("%d ")
        date_today_1 = (datetime.date.today() + datetime.timedelta(-1) + datetime.timedelta(day_delta)).strftime("%d ")
        print(date_today)
        for line in lines:
            if date_today in line :
                # print(date_today)
                matchObj = re.search( r'.*BUSD止盈.*', line)
                if matchObj:
                    zhiying_count+=1
                    profit_sum+=1
                    # print("match --> : ", matchObj.group())
            if date_today_1 in line :
                # print(line)
                matchObj = re.search( r'.*BUSD止盈.*', line)
                if matchObj:
                    # zhiying_count+=1
                    pass
                    # print("match --> : ", matchObj.group())
            

            if date_today in line :
                # print(line)
                matchObj = re.search( r'.*BUSD止损.*', line)
                if matchObj:
                    zhisun_count+=1
                    tot_zhisun+=1
                    # print("match --> : ", matchObj.group())
        print(date_today)
        print("今昨止盈数"+str(zhiying_count),end='  ')
        print("今日止损数"+str(zhisun_count))
        print()
        x.append(date_today)
        y.append(zhiying_count)
        z.append(zhisun_count)
        s.append(zhiying_count-zhisun_count*2)
        if len(ss)>0:
            ss.append(ss[-1]+s[-1])
        else:
            ss.append(s[0])
        print(s)
        print(ss)
    print("最终止盈数:"+str(profit_sum))
    print("最终止损数:"+str(tot_zhisun))

    import matplotlib.pyplot as plt
 
    fig,(ax1,ax2,ax3) = plt.subplots(3,1)
    # 设置标题和标签
    bar1=ax1.bar(x, y)
    ax1.set_title('TP_count Chart')
    ax1.set_xlabel('X Label')
    ax1.set_ylabel('TP_count')

    bar2=ax2.bar(x, z)
    ax2.set_title('SL_count Chart')
    ax2.set_xlabel('X Label')
    ax2.set_ylabel('SL_count')

    bar3=ax3.bar(x, s)
    ax3.set_title('profit_count Chart')
    ax3.set_xlabel('X Label')
    ax3.set_ylabel('profit_count')

    # bar4=ax4.bar(x, ss)
    # ax4.set_title('profit_acum Chart')
    # ax4.set_xlabel('X Label')
    # ax4.set_ylabel('profit_acum')

    # 显示数值
    for bar in bar1:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width() / 2.0, height, str(height), ha='center', va='bottom')
    # plt.tight_layout()
        # 显示数值
    for bar in bar2:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width() / 2.0, height, str(height), ha='center', va='bottom')

        # 显示数值
    for bar in bar3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width() / 2.0, height, str(height), ha='center', va='bottom')

    #     # 显示数值
    # for bar in bar4:
    #     height = bar.get_height()
    #     ax4.text(bar.get_x() + bar.get_width() / 2.0, height, str(height), ha='center', va='bottom')

    plt.tight_layout()
    # 显示图形
    plt.show()


def send_email(mail_msg:str,mail_title:str='数字货币_活跃交易'):

    # qq邮箱smtp服务器
    host_server = 'smtp.qq.com'
    # sender_qq为发件人的qq号码
    sender_qq = '1324907549'
    # pwd为qq邮箱的授权码
    pwd = 'orkbhcwvxpuljbfe'
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
    path = "new_msg_id_folder"
    if sys.platform=='linux':
        path = "/root"
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        log("初次部署,信息缓存文件"+path+'不存在')
        # 创建目录操作函数
        os.makedirs(path,mode=0x777,exist_ok=True)
        log("信息缓存文件夹"+ path + ' 创建成功')

    file = open(path+'/'+exc_name+"_new_msg_id.txt", "r+") #r+ 和w+ 都具有读写权限，w+在NULL会新创建新文件，原始内容抹除
    last_msg_id = file.readline()
    print("读取消息id" +last_msg_id)
    if last_msg_id != msg_id:
        file = open(path + '/' + exc_name + "_new_msg_id.txt", "w+") #重新创建一个同名空文件覆盖，写入，相当于删除了旧消息
        # file.seek(0,0)
        file.write(str(msg_id))
        file.close()
        return True
    else:
        return False

def read_news_title_with_speaker(texts:str="测试文本"):
    # 模块初始化
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    print(rate)
    engine.setProperty('rate', rate - 50)
    # 设置发音大小，范围为0.0-1.0
    volume = engine.getProperty('volume')
    engine.setProperty('volume', 0.7)
    # 男生普通话发音
    engine.setProperty(
        'voice', "com.apple.speech.synthesis.voice.ting-ting.premium")
    # 添加朗读文本
    engine.say(texts)
    # 等待语音播报完毕
    engine.runAndWait()

def exch_to_chinese(exc_name_en):
    # dic={"Binance":"币安", "FTX": "FTX", "KuCoin":"酷币","Gate.io":"Gate io",
    #      "Huobi": "火币","OKEx":"欧易","Coinbase Pro (GDAX)":"Coinbase"}
    if exc_name_en=="Binance":
        return "币安"
    elif exc_name_en=="FTX":
        return "FTX"
    elif exc_name_en=="KuCoin":
        return "酷币"
    elif exc_name_en=="Gate.io":
        return "芝麻开门"
    elif exc_name_en=="Huobi":
        return "火币"
    elif exc_name_en=="OKEx":
        return "欧易"
    elif exc_name_en=="Coinbase Pro (GDAX)":
        return "Coinbase"
    else:
        return "错误的交易所名称"


def SMA(data, smaPeriod):
    sma = []
    count = 0
    for i in range(len(data)):
        if data[i] is None:
            sma.append(None)
        else:
            count += 1
            if count < smaPeriod:
                sma.append(None)
            else:
                sma.append(np.mean(data[i-smaPeriod+1:i+1]))

    return np.array(sma)





def simu_test_real_with_stop(file_name:str="",stop_profit_count=1):
    pre_path = "log"
    if sys.platform=='linux':
        pre_path = "/root"
    log_f_path = pre_path+'/'+file_name #全路径
    if not os.path.exists(log_f_path):
        print("文件不存在.."+log_f_path)
    else:
        file = open(log_f_path, "r")  # 1.读写,追加
    print("读取日志:")
    lines = file.readlines()    # 接收数据

    profit_sum = 0
    tot_zhisun =0
    x = []
    y = []
    z = []
    s = []
    ss= []
    sum=0
    for day_delta in range(-60,0):
        zhiying_count=0
        zhisun_count=0
        date_today = (datetime.datetime.now() + datetime.timedelta(day_delta)).strftime("%m-%d ")
        date_today_1 = (datetime.date.today() + datetime.timedelta(-1) + datetime.timedelta(day_delta)).strftime("%m-%d ")
        print(date_today)
        for line in lines:
            if date_today in line :
                # print(date_today)
                matchObj = re.search( r'.*BUSD止盈.*', line)
                if matchObj:
                    zhiying_count+=1
                    profit_sum+=1
                    print("match --> : ", matchObj.group())
            if date_today_1 in line :
                # print(line)
                matchObj = re.search( r'.*BUSD止盈.*', line)
                if matchObj:
                    # zhiying_count+=1
                    pass
                    # print("match --> : ", matchObj.group())
            

            if date_today in line :
                # print(line)
                matchObj = re.search( r'.*BUSD止损.*', line)
                if matchObj:
                    zhisun_count+=1
                    tot_zhisun+=1
                    print("match --> : ", matchObj.group())
        print(date_today)
        print("今昨止盈数"+str(zhiying_count),end='  ')
        print("今日止损数"+str(zhisun_count))
        print()
        x.append(date_today)
        y.append(zhiying_count)
        z.append(zhisun_count)
        s.append(zhiying_count-zhisun_count*2)
        sum+=zhiying_count-zhisun_count*2
        sum_tmp=sum
        if len(ss)>0:
            ss.append(sum_tmp)
        else:
            ss.append(sum_tmp)
        print(s)
        print(ss)
    print("最终止盈数:"+str(profit_sum))
    print("最终止损数:"+str(tot_zhisun))

    import matplotlib.pyplot as plt
 
    fig,(ax3,ax4) = plt.subplots(2,1)
    # # 设置标题和标签
    # bar1=ax1.bar(x, y)
    # ax1.set_title('TP_count Chart')
    # ax1.set_xlabel('X Label')
    # ax1.set_ylabel('TP_count')

    # bar2=ax2.bar(x, z)
    # ax2.set_title('SL_count Chart')
    # ax2.set_xlabel('X Label')
    # ax2.set_ylabel('SL_count')

    bar3=ax3.bar(x, s)
    ax3.set_title('profit_count Chart')
    ax3.set_xlabel('X Label')
    # ax3.set_ylabel('profit_count')

    bar4=ax4.plot(x, ss)
    ax4.set_title('profit_acum Chart')
    ax4.set_xlabel('X Label')
    # ax4.set_ylabel('profit_acum')

    # # 显示数值
    # for bar in bar1:
    #     height = bar.get_height()
    #     ax1.text(bar.get_x() + bar.get_width() / 2.0, height, str(height), ha='center', va='bottom')
    # # plt.tight_layout()
    #     # 显示数值
    # for bar in bar2:
    #     height = bar.get_height()
    #     ax2.text(bar.get_x() + bar.get_width() / 2.0, height, str(height), ha='center', va='bottom')

        # 显示数值
    for bar in bar3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width() / 2.0, height, str(height), ha='center', va='bottom')

        # 显示数值
    # for bar in bar4:
    #     height = 200#bar.get_height()
    #     width = 30#bar.get_width()
       
        # ax4.text(bar.get_x() + width/2.0, height, str(height), ha='center', va='bottom')
    plt.xticks(rotation=270)
    for i in range(len(ss)):
        ax4.annotate("{:.2f}".format(ss[i]), xy=(x[i], ss[i]), color='red')
        plt.tight_layout()
    # 调整图形与屏幕左右的间隙
    # plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)
    # 显示图形
    plt.show()


def simu_test_real(file_name:str="",stop_profit_count=1):
    pre_path = "log"
    if sys.platform=='linux':
        pre_path = "/root"
    log_f_path = pre_path+'/'+file_name #全路径
    if not os.path.exists(log_f_path):
        print("文件不存在.."+log_f_path)
    else:
        file = open(log_f_path, "r")  # 1.读写,追加
    print("读取日志:"+file_name)
    lines = file.readlines()    # 接收数据

    profit_sum = 0
    tot_zhisun =0
    x = []
    y = []
    z = []
    s = []
    ss= []
    sum=0
    for day_delta in range(-60,0):
        zhiying_count=0
        zhisun_count=0
        date_today = (datetime.datetime.now() + datetime.timedelta(day_delta)).strftime("%m-%d ")
        date_today_1 = (datetime.date.today() + datetime.timedelta(-1) + datetime.timedelta(day_delta)).strftime("%m-%d ")
        print(date_today)
        for line in lines:
            if date_today in line :
                # print(date_today)
                matchObj = re.search( r'.*BUSD止盈.*', line)
                if matchObj:
                    zhiying_count+=1
                    profit_sum+=1
                    print("match --> : ", matchObj.group())
            if date_today_1 in line :
                # print(line)
                matchObj = re.search( r'.*BUSD止盈.*', line)
                if matchObj:
                    # zhiying_count+=1
                    pass
                    # print("match --> : ", matchObj.group())
            

            if date_today in line :
                # print(line)
                matchObj = re.search( r'.*BUSD止损.*', line)
                if matchObj:
                    zhisun_count+=1
                    tot_zhisun+=1
                    print("match --> : ", matchObj.group())
        print(date_today)
        print("今昨止盈数"+str(zhiying_count),end='  ')
        print("今日止损数"+str(zhisun_count))
        print()
        x.append(date_today)
        y.append(zhiying_count)
        z.append(zhisun_count)
        s.append(zhiying_count-zhisun_count*2)
        sum+=zhiying_count-zhisun_count*2
        sum_tmp=sum
        if len(ss)>0:
            ss.append(sum_tmp)
        else:
            ss.append(sum_tmp)
        print(s)
        print(ss)
    print("最终止盈数:"+str(profit_sum))
    print("最终止损数:"+str(tot_zhisun))

    import matplotlib.pyplot as plt
 
    fig,(ax3,ax4) = plt.subplots(2,1)
    # # 设置标题和标签
    # bar1=ax1.bar(x, y)
    # ax1.set_title('TP_count Chart')
    # ax1.set_xlabel('X Label')
    # ax1.set_ylabel('TP_count')

    # bar2=ax2.bar(x, z)
    # ax2.set_title('SL_count Chart')
    # ax2.set_xlabel('X Label')
    # ax2.set_ylabel('SL_count')

    bar3=ax3.bar(x, s)
    ax3.set_title('profit_count Chart')
    ax3.set_xlabel('X Label')
    # ax3.set_ylabel('profit_count')

    bar4=ax4.plot(x, ss)
    ax4.set_title('profit_acum Chart')
    ax4.set_xlabel('X Label')
    # ax4.set_ylabel('profit_acum')

    # # 显示数值
    # for bar in bar1:
    #     height = bar.get_height()
    #     ax1.text(bar.get_x() + bar.get_width() / 2.0, height, str(height), ha='center', va='bottom')
    # # plt.tight_layout()
    #     # 显示数值
    # for bar in bar2:
    #     height = bar.get_height()
    #     ax2.text(bar.get_x() + bar.get_width() / 2.0, height, str(height), ha='center', va='bottom')

        # 显示数值
    for bar in bar3:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width() / 2.0, height, str(height), ha='center', va='bottom')

        # 显示数值
    # for bar in bar4:
    #     height = 200#bar.get_height()
    #     width = 30#bar.get_width()
       
        # ax4.text(bar.get_x() + width/2.0, height, str(height), ha='center', va='bottom')
    plt.xticks(rotation=270)
    for i in range(len(ss)):
        ax4.annotate("{:.2f}".format(ss[i]), xy=(x[i], ss[i]), color='red')
        plt.tight_layout()
    # 调整图形与屏幕左右的间隙
    # plt.subplots_adjust(left=0.1, bottom=0.1, right=0.9, top=0.9)
    # 显示图形
    plt.show()


if __name__ == '__main__':
    # send_email(" 尝试启动 交易对 BUSD_TLM ")
    # read_news_title_with_speaker("test")
    # log_to_file("新币上线","lastest_news_bbb")
    # date=[1,2,4,8,16,32,64,128,256,512]
    # sma=SMA(date,2)
    # sma=[1,2,4,6,8,10,12,14,16,18]
    # print(sma)
    # SMA_ank(sma,7)

    # log_to_file_path = "5UP_filter_30mtp_5_10_white_no_liandan_no_jixian_1klinedelay.log"
    # log_to_file_path="5UP_filter_30mtp_5_10_white_no_liandan_no_jixian.log"
    log_to_file_path="5UP_filter_30mtp_5_10MA_duotou_white.log" 
    # log_to_file_path="5UP_filter_30mtp_5_10_white.log" 
    # log_to_file_path="5UP_filter_15m_first_lony_top10.log" 
    # read_log_file_last_profit_count(log_to_file_path)
    # parse_log_file_last_profit_count(log_to_file_path)
    simu_test_real(log_to_file_path)


