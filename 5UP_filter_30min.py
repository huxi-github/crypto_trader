# encoding: utf-8
from playsound import playsound

from py3commas.request import Py3Commas
from util import log_to_file,log, send_email, read_news_title_with_speaker
import datetime
import time
from config import *

import pandas as pd

#全局可持久化变量
sel_coin_global=[]
Entry_pri={"BTCUSDT":30000}
Last_Entry_TICKDate={"BTCUSDT":"2020-03-12 15:22:00"}
# inital_dollers =10000
# current_balance =inital_dollers
Staic={"inital_dollers":10000,"current_balance":10000,"win_count":0,"lose_count":0}


#配置数据:策略
SP_per =4
SL_per =11
Frame_level= '30m'
log_to_file_path = "5UP_filter_"+Frame_level+".log"
golobal_data ="golobal_data"+Frame_level


#速度配置
POLL_INTERVAL_IN_SEC =60*15
SCAN_NEW_ARTI_INTERVAL_IN_SEC =60*5
CHOSE_RANGE=50

# 6615账户的 key 和 secr
p3c = Py3Commas(key='xxx',
                secret='xxx'
                       ' '
                       ' '
                       ' ')

# ///////GET /api/v3/ticker/24hr
def get_top_coin():
    data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/ticker/24hr"
            )
    # if 'net_erro' in data_arry:
    #
    i=0
    sorted_arry = sorted(data_arry, key = lambda i: float(i['priceChangePercent']),reverse = True)
    print("24H 涨幅榜前20:")
    print('rank"\tsymbol_name ' + "\t\t\t" + 'priceChangePercent')
    top_hot_symbol={}
    for symbl_d in sorted_arry:
        if symbl_d['symbol'].endswith("BUSD") :
            # 排除PULL DOWN  类型
            if "BULL" in symbl_d['symbol'] or "DOWN" in symbl_d['symbol']: continue
            print(str(i)+ "\t\t" + symbl_d['symbol'] + "\t\t\t\t\t" + symbl_d['priceChangePercent'])
            i = i + 1
            top_hot_symbol[symbl_d['symbol']]=symbl_d['priceChangePercent']
            if i>=CHOSE_RANGE: break
    return top_hot_symbol


# ///////GET /api/v3/klines
def get_symbol_change_of_last_frame_s(symbol:str="",watch_interval:str="5m",limit:str='0'):
    data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/klines",
            params="symbol="+symbol+"&interval="+watch_interval+"&limit="+limit
            #params="symbol=C98USDT&interval=5m&limit=3"         #一个符号
            )

    symbl_d = data_arry[0]
    open = float(symbl_d[1])
    high = float(symbl_d[2])
    low  = float(symbl_d[3])
    close= float(symbl_d[4])
    price_change_max_percent = 100.00*(high-low)/open
    price_change_percent= 100.00*(close-open)/open
    print("open:"+str(open))
    print("close:" + str(close))
    #close即是 当前价格
    print("交易对"+symbol+" 在最近"+str(limit)+"个"+watch_interval+"内变化:"+ str(price_change_percent)[:4] +"%"+"\t振幅变化:" + str(price_change_max_percent)[:4] +"%")
    return price_change_percent


# def do_10_continous_up_Analysis(symbol:str=""):
#     limit=15
#     watch_interval='1m'
#     data_arry = p3c.request_binance_data(
#             http_method="GET",
#             path="/api/v3/klines",
#             params="symbol="+symbol+"&interval="+watch_interval+"&limit="+str(limit)
#             #params="symbol=C98USDT&interval=5m&limit=3"         #一个符号
#             )
#     conti_up_cnt=0
#     for i in range(limit):
#         data = data_arry[i]
#         open = float(data[1])
#         high = float(data[2])
#         low  = float(data[3])
#         close= float(data[4])
#         price_change_percent= 100.00*(close-open)/open
#         print("open:"+str(open))
#         print("close:" + str(close))
#         print("price_change_percent="+str(price_change_percent))
#         if 0<price_change_percent and price_change_percent<1.5:
#             conti_up_cnt+=1
#         #close即是 当前价格
#     print("交易对"+symbol+" 在最近前"+str(limit)+"个"+watch_interval+"内 增长分钟数为"+str(conti_up_cnt))
#     if conti_up_cnt>10:
#         return True
#     else:
#         return False

def do_MA_condition_Analysis(data):
    #是否在30 均线上方
    print(data.iloc[-5]['MA30'])
    if float(data.iloc[-6]['Close'])  > float(data.iloc[-6]['MA30'])and float(data.iloc[-5]['Close'])  > float(data.iloc[-5]['MA30'])\
    and float(data['Close'].iloc[-4]) > float(data['MA30'].iloc[-4]) and float(data['Close'].iloc[-3]) > float(data['MA30'].iloc[-3])\
    and float(data['Close'].iloc[-2]) > float(data['MA30'].iloc[-2])\
    and float(data['Close'].iloc[-1]) > float(data['MA30'].iloc[-1]):# and  float(data['Close'].iloc[-1]) > float(data['MA30'].iloc[-1]):
        return True
    else:
        return False

def do_cacu_MA_last5(sysbol_pair:str,frame_level:str):
    data=get_symbol_data_of_last_frame_s(sysbol_pair,frame_level,'105')
    MA7_s = data['Close'][-(7+6):].rolling(7).mean()
    MA30_s = data['Close'][-(30+6):].rolling(30).mean() #data['SMA30']#
    MA99_s = data['Close'][-(99+6):].rolling(99).mean()
    data['MA7'] =  MA7_s
    data['MA30'] = MA30_s
    data['MA99'] = MA99_s
    return data


# ///////GET /api/v3/klines
def get_symbol_data_of_last_frame_s(symbol:str="",watch_interval:str="1h",limit:str='99'):
    data_list_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/klines",
            params="symbol="+symbol+"&interval="+watch_interval+"&limit="+limit
            )
    names=['Date', 'Open','High','Low','Close','Volume','close_Date','volume_usdt','8','9','10','11']
    pd_data = pd.DataFrame(data_list_arry)
    pd_data.columns= names
    return pd_data #所有的收盘价

def do_the_select_and_decision_fast():
    cur_time = datetime.datetime.now().strftime("%H:%M")
    log("current time is " + cur_time + "trying to get_top_15_symbol")
    top_symbols = get_top_coin()

    # sel = []
    # start for loop
    for (key, val) in top_symbols.items():
        coin_pair = str(key)
        ''' 注释
        price_change_2H = get_symbol_change_of_last_frame(coin_pair, "2H")
        if  -10 < price_change_2H and price_change_2H < -5:  #  2H 涨幅
            print(" 2H 涨幅不符合条件")
            continue
        '''
        '''
        最后两分钟 ，超长拉升>%3 则不入
        '''
        # "ALICEBUSD", "15m"

        data = do_cacu_MA_last5(coin_pair, Frame_level)
        five_UP = do_5_continous_up_Analysis(data)
        One_KLine_Same_Entry =False
        if coin_pair in Last_Entry_TICKDate and Last_Entry_TICKDate[coin_pair] == pd.to_datetime(data['Date'].iloc[-1]/1000,unit='s'):
            One_KLine_Same_Entry =True
            print("同一根K线重复进入")
        if five_UP and do_MA_condition_Analysis(data) and not One_KLine_Same_Entry: 
            print(coin_pair+"符合5UP条件，启动的的交易符号："+str(sel_coin_global))
            if not coin_pair in sel_coin_global:
                sel_coin_global.append(coin_pair)
                Entry_pri[coin_pair] = float(data["Close"].iloc[-1])
                Last_Entry_TICKDate[coin_pair] = pd.to_datetime(data['Date'].iloc[-1]/1000,unit='s')
                log_to_file(coin_pair + "符合5UP条件@"+str(Entry_pri[coin_pair])+"启动的交易符号：" + str(sel_coin_global),log_to_file_path)
                do_data_store()
        else:
            print(coin_pair + "不符合5UP条件")
        # if len(sel)>=1:
            # read_news_title_with_speaker("同时上涨数量15分之"+str(len(sel))+"个,行情可能转好...")
        do_deal_finish_check(data,coin_pair)
        time.sleep(2)

def do_5_continous_up_Analysis(data):
    if data['Close'].iloc[-6] < data['Close'].iloc[-5]\
    and data['Close'].iloc[-5] < data['Close'].iloc[-4] \
    and data['Close'].iloc[-4] < data['Close'].iloc[-3] \
    and data['Close'].iloc[-3] < data['Close'].iloc[-2]:
    # and data['Close'].iloc[-2] < data['Close'].iloc[-1]:# ['Close'].iloc[-1] 时刻变化的，就是最新价格
        return True
    else:
        return False

def do_deal_finish_check(data,coin_pair):
    global sel_coin_global
    if coin_pair in sel_coin_global:
        global Entry_pri,Staic
        if float(data['High'].iloc[-1]) > Entry_pri[coin_pair]*(100+SP_per)/100:
            print(coin_pair+"止盈@"+str(Entry_pri[coin_pair]*(100+SP_per)/100))
            print("befor add"+str(Staic['win_count']))
            Staic['win_count'] = Staic['win_count'] + 1
            print("after add"+str(Staic['win_count']))
            log_to_file(coin_pair + "止盈+++++@"+str(Entry_pri[coin_pair]*(100+SP_per)/100), log_to_file_path)
            log_to_file("策略盈利"+str(Staic['win_count'])+"次  止损"+str(Staic['lose_count'])+"次", log_to_file_path)
            sel_coin_global.remove(coin_pair)
            del Entry_pri[coin_pair]
            do_data_store()
        elif float(data['Low'].iloc[-1]) < Entry_pri[coin_pair]*(100-SL_per)/100:
            print(coin_pair+"止损@"+str(Entry_pri[coin_pair]*(100-SL_per)/100))
            Staic['lose_count'] = Staic['lose_count'] + 1
            log_to_file(coin_pair + "止损——————@"+str(Entry_pri[coin_pair]*(100-SL_per)/100), log_to_file_path)
            log_to_file("策略盈利"+str(Staic['win_count'])+"次  止损"+str(Staic['lose_count'])+"次", log_to_file_path)
            sel_coin_global.remove(coin_pair)
            del Entry_pri[coin_pair]
            do_data_store()


def do_data_store():
    import shelve
    print("持久化")
    with shelve.open(golobal_data) as db:
        db['sel_coin_global'] = sel_coin_global
        db['Entry_pri'] = Entry_pri
        db['Staic'] = Staic
        db['Last_Entry_TICKDate'] = Last_Entry_TICKDate

def init_form_data_store():
    import shelve
    print("初始化历史数据...")
    with shelve.open(golobal_data) as db:
        global sel_coin_global,Entry_pri,Staic,Last_Entry_TICKDate
        if 'sel_coin_global' in db:
            sel_coin_global = db['sel_coin_global']
            print("set sel_coin_global="+str(sel_coin_global))
        if 'Entry_pri' in db:
            Entry_pri = db['Entry_pri'] 
            print("set Entry_pri="+str(Entry_pri))
        if 'Staic' in db:
            Staic = db['Staic']
            print("set Staic="+str(Staic))
        if 'Last_Entry_TICKDate' in db:
            Last_Entry_TICKDate = db['Last_Entry_TICKDate']
            print("set Last_Entry_TICKDate="+str(Last_Entry_TICKDate))



if __name__ == '__main__':
    #  拉盘启动模拟账户交易
    #意外终止读取 上次存储的数据
    init_form_data_store() 
    # print("------- Entry_pri="+str(Entry_pri))
    # print("------- sel_coin_global="+str(sel_coin_global))
    # print("------- Staic="+str(Staic))
    # print("------- Last_Entry_TICKDate="+str(Last_Entry_TICKDate))
    while (True):
        '''
        时间判断 8：am  and 18：pam
        '''
        # do_time_period_select()
        do_the_select_and_decision_fast()
        log("等待 " + str(POLL_INTERVAL_IN_SEC / 60) + "min 再次查找")
        time.sleep(POLL_INTERVAL_IN_SEC)






    # data = get_symbol_data_of_last_frame_s("JASMYBUSD", "1h", '105')
    # print(data["Close"].iloc[-2])