from playsound import playsound

from py3commas.request import Py3Commas
from util import log, send_email, read_news_title_with_speaker
import datetime
import time
from config import *

POLL_INTERVAL_IN_SEC =3
SCAN_NEW_ARTI_INTERVAL_IN_SEC =60*5
#6615账户的 key 和 secr
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
    print("24H 涨幅榜前5:")
    print('rank"\tsymbol_name ' + "\t\t\t" + 'priceChangePercent')
    top_hot_symbol={}
    for symbl_d in sorted_arry:
        if symbl_d['symbol'].endswith("BUSD") :
            if "BULL" in symbl_d['symbol'] or "DOWN" in symbl_d['symbol']: continue
            print(str(i)+ "\t\t" + symbl_d['symbol'] + "\t\t\t\t\t" + symbl_d['priceChangePercent'])
            i = i + 1
            top_hot_symbol[symbl_d['symbol']]=symbl_d['priceChangePercent']
            if i>=15: break
    return top_hot_symbol


def get_fast_change_coin_15m():
    top_symbols = get_top_coin()
    i = 0
    for (key, val) in top_symbols.items():
        coin_pair = key
        tv_url = "https://cn.tradingview.com/chart/oLP03YDC/"
        # send_email(cur_time + " 今日交易对" + coin_pair+ " 24H 涨幅:"+top_symbols[key]+"%\n"+tv_url)
        # update_bot_pairs(coin_pair, "5150456")
        # i = i + 1
        # if i >= 2: break
        re = get_coin_stat(coin_pair,"15m",4)
        print(coin_pair + "is fast coin? re="+str(re))


# ///////GET /api/v3/klines
def get_coin_stat(symbol:str="",watch_interval:str="5m",limit:int=3):
    params_str= "symbol="+symbol+"&interval="+watch_interval+"&limit="+str(limit)
    data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/klines",
            params=params_str   # params="symbol=C98USDT&interval=5m&limit=3"         #一个符号
            )
    i=0
    sustain_n=0
    am_sustain_n=0
    for symbl_d in data_arry:
        open = float(symbl_d[1])
        high = float(symbl_d[2])
        low  = float(symbl_d[3])
        close= float(symbl_d[4])
        price_change_max_percent = 100.00*(high-low)/open
        price_change_percent= 100.00*(close-open)/open
        i = i + 1
        if price_change_percent>2:
            sustain_n = sustain_n + 1
            # print("连续"+str(sustain_n)+ "个5min 上涨超2%")
        if price_change_max_percent>2 or price_change_max_percent <-2:
            am_sustain_n = am_sustain_n + 1
            # print("连续"+str(am_sustain_n)+ "个5min 振幅超2%")     # sorted_arry = sorted(data_arry, key = lambda i: float(i['priceChangePercent']),reverse = True)
    print("交易对"+symbol+" 在最近"+str(limit)+" 个"+watch_interval+"内超幅上涨2%的次数为"+str(sustain_n) +"/"+str(limit))
    print("交易对"+symbol+" 在最近"+str(limit)+" 个"+watch_interval+"内振幅变化2%的次数为"+str(am_sustain_n) +"/"+str(limit))
    if sustain_n>2*limit/3:
        return True
    else:
        return False



    symbl_d = data_arry[0]
    open = float(symbl_d[1])
    high = float(symbl_d[2])
    low  = float(symbl_d[3])
    close= float(symbl_d[4])
    price_change_max_percent = 100.00*(high-low)/open
    price_change_percent= 100.00*(close-open)/open
    print("open:"+str(open))
    print("close:" + str(close))#close即是 当前价格
    print("交易对"+symbol+" 在最近1个"+watch_interval+"内变化:"+ str(price_change_percent)[:4] +"%"
                                                +"\t振幅变化:" + str(price_change_max_percent)[:4] +"%")
    return price_change_percent


# ///////GET /api/v3/klines
def get_symbol_MA_of_last_frame_s(symbol:str="",watch_interval:str="5m",limit:str='0'):
    data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/klines",
            params="symbol="+symbol+"&interval="+watch_interval+"&limit="+limit
            )
    close_sum =0.0
    for data in data_arry:
        symbl_d = data
        close= float(symbl_d[4])
        close_sum = close_sum+close
    close_ave=close_sum/float(limit)
    #close即是 当前价格
    print("交易对"+symbol+" 在最近"+str(limit)+"个"+watch_interval+" MA"+limit+":="+str(close_ave))
    return close_ave

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

def print_symbol_change_rank_of_frame(watch_interval:str="15m",top_symbols=None):
    symbol_arr={}
    for (key, val) in top_symbols.items():
        coin_pair = key
        price_change_percent = get_symbol_change_of_last_frame(coin_pair,watch_interval)
        symbol_arr[coin_pair] = price_change_percent
    sorted_arry = sorted(symbol_arr.items(), key = lambda i: float(i[1]),reverse = True)
    print("TOP5 "+watch_interval+"内变化榜:")
    #打印15min排行榜
    for (key, val) in sorted_arry:
        print(key +"   "+str(val)[:4]+"%")
    print()




def start_just_one_deal_of_pair_muti_bot(coin_pair:str=""):
    # print("砸盘超6% ，实际幅度为:" + str(val)[:4] + "%"
    #            +"收到推送后现在 tradingview 上观察 模拟一两天，几次之后再实盘 稳重的话，一个符号一单，再换其他pump symbol"
    #            +"1.观察1.TV 1h量化图，处于 上升期 还是 下跌期 \n 2.24H 涨幅  \n3.单日大盘行情 \n4."
    #             "回调距离成本线距离，SO的大小>4 目前模拟结果，问题较大\n"
    #             "查看实时模拟:https://cn.tradingview.com/chart/oLP03YDC/?symbol=BINANCE%3A"+key)

    print("开启mutil-pair-bot 一单，交易对:" + coin_pair)
    # sprint("开启mutil-pair-bot 一单，交易对:" + coin_pair)
    # log_deal_to_log_file_with_time()
    log("模拟账户同时创建订单"+coin_pair)
    start_new_deal_test_account(coin_pair)

    # MA_OK=do_MA_condition_Analysis(coin_pair,"15m")
    # if not  MA_OK:
    #     index_s = coin_pair.find("BUSD")
    #     base = list(coin_pair[0:index_s])
    #     send_email("货币【_" + str(base) + "】符合3个条件,不符合15分钟MA条件，交易放弃")
    #     # read_news_title_with_speaker("货币【_" + str(base) + "】符合3个条件,但不符合15分钟M A条件，交易放弃")
    #     return

    start_new_deal(coin_pair)
    # ////// 打印该币 是否支持杠杆---
    # playsound("audio/notification.wav")
    index_s = coin_pair.find("BUSD")
    base = list(coin_pair[0:index_s])
    # read_news_title_with_speaker("币种【_" + str(base) + "】符合3个条件MA判断,启动交易")



def get_anooucement_1h():

    data_arry = p3c.get_binance_web_data(
            http_method="GET",
            path="/bapi/composite/v1/public/cms/article/catalog/list/query",
            params="catalogId=48&pageNo=1&pageSize=2"
            )

    articles = data_arry['data']['articles']
    if not check_and_update_msg(str(articles[0]['id'])):
        print("没有新文章")
        return
    for arti in articles:
        id = arti['id']
        title =arti['title']
        log("id:"+str(id))
        log("title:" + title)

# ///////GET /api/v3/klines
def get_symbol_change_of_last_frame(symbol:str="",watch_interval:str="5m"):
    data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/klines",
            params="symbol="+symbol+"&interval="+watch_interval+"&limit="+str(1)
            )

    if 'net_erro' in data_arry:
        print("网络错误")
        return -1
    symbl_d = data_arry[0]
    open = float(symbl_d[1])
    high = float(symbl_d[2])
    low  = float(symbl_d[3])
    close= float(symbl_d[4]) # close==cur_price
    price_change_max_percent = 100.00*(high-low)/open
    price_change_percent= 100.00*(close-open)/open
    print("open:"+str(open))
    print("close:" + str(close))#close即是 当前价格
    print("交易对"+symbol+" 在最近1个"+watch_interval+"内变化:"+ str(price_change_percent)[:4] +"%"
                                                +"\t振幅变化:" + str(price_change_max_percent)[:4] +"%")
    return price_change_percent

def check_and_update_msg(msg_id:str="kong msg"):
    file = open("msg_new_id.txt", "r+")
    last_msg_id = file.readline()
    print("读取第一行" +last_msg_id)
    if last_msg_id != msg_id:
        file.seek(0,0)
        file.write(str(msg_id))
        file.close()
        return True
    else:
        return False

def do_10_continous_up_Analysis(symbol:str=""):
    limit=15
    watch_interval='1m'
    data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/klines",
            params="symbol="+symbol+"&interval="+watch_interval+"&limit="+str(limit)
            #params="symbol=C98USDT&interval=5m&limit=3"         #一个符号
            )
    conti_up_cnt=0
    for i in range(limit):
        data = data_arry[i]
        open = float(data[1])
        high = float(data[2])
        low  = float(data[3])
        close= float(data[4])
        price_change_percent= 100.00*(close-open)/open
        print("open:"+str(open))
        print("close:" + str(close))
        print("price_change_percent="+str(price_change_percent)) 
        if 0<price_change_percent and price_change_percent<1.5:
            conti_up_cnt+=1
        #close即是 当前价格
    print("交易对"+symbol+" 在最近前"+str(limit)+"个"+watch_interval+"内 增长分钟数为"+str(conti_up_cnt))
    if conti_up_cnt>10:
        return True
    else:
        return False

def do_MA_condition_Analysis(sysbol_pair:str,frame_level:str="15m"):
    MA7=get_symbol_MA_of_last_frame_s(sysbol_pair,frame_level,'7')
    MA25=get_symbol_MA_of_last_frame_s(sysbol_pair,frame_level,'25')
    MA99=get_symbol_MA_of_last_frame_s(sysbol_pair,frame_level,'99')
    if MA7>MA25 and MA25>MA99:
        return True
    else:
        return False

def do_the_select_and_decision_fast():
    cur_time = datetime.datetime.now().strftime("%H:%M")
    log("current time is " + cur_time + "trying to get_top_5_symbol")
    top_symbols = get_top_coin()

    sel = []
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
        低于24 H HIGH  15% 的拉升不要进去，骗炮
        '''

        '''八连阳，则不入'''

        '''
        三连阳 均属于 1%-2%  则入，暴风雨的初期
        '''

        '''
        最后两分钟 ，超长拉升>%3 则不入
        '''

        '''
        达到最大交易数，检查 当前reserved 的资金数目，如果超过 多少，心理风险过大，则暂停一段时间再检查和启动
        '''

        '''本币种的USDT 交易对在上新，对比的拉升'''

        price_change_15m = get_symbol_change_of_last_frame(coin_pair, "15m")
        if price_change_15m > 4 and price_change_15m < 50:#(<50%排除新币上线的单当 天情况，新上线的新币不会再 备选表里面，)
            price_change_5m = get_symbol_change_of_last_frame(coin_pair, "5m")
            if  price_change_5m > 2  :
                price_change_1m = get_symbol_change_of_last_frame(coin_pair, "1m")
                if price_change_1m > 0.3 and price_change_1m < 10: #(<10% 反向插针，诱高的情况)
                    sel.append(coin_pair)
                    if do_10_continous_up_Analysis(coin_pair):
                        print("交易对【"+coin_pair+"】开始震荡上升")
                        read_news_title_with_speaker("交易对【"+coin_pair+"】疑似连阳缓慢上升")
                    # read_news_title_with_speaker("交易对【"+coin_pair+"】开始震荡上升")
                    # print("交易对【" + coin_pair + "】符合3个条件，直接启动交易")===>开启的交易对放在一个log 里面
                else:
                    print("1min涨幅不符合条件")
            else:
                print("5min涨幅不符合条件")
        else:
            print("15min涨幅不符合条件")
    #end for loop
    print("本符合条件，启动的的交易符号："+str(sel))
    if len(sel)>=2:
        read_news_title_with_speaker("同时上涨数量15分之"+str(len(sel))+"个,行情可能转好...")

# if __name__ == '__main__':
    # get_top_coin()
    # start_new_deal("USDT_BTC")
    # update_bot_pairs("USDT_BTC","5150456")
    # get_fast_change_coin()  # 思路，，，前10名 里面进进行筛选
    # get_fast_change_coin_1m()
    # get_symbol_change_of_last_frame("ALICEBUSD","15m")
    # re = get_coin_static("HEGICBUSD", "3m", 20)
    # ------上市通知警告
    # while(True):

    #     time.sleep(SCAN_NEW_ARTI_INTERVAL_IN_SEC)
    # 交易所 大挂单 分析==>辅助压力线，//////



if __name__ == '__main__':
    #-----15 min 拉盘启动模拟账户交易
    # [new deal 条件 1.15min 6%up  2.10min 2%up （3)3min 1.5%  (4)1min 1% up]  （5）信号其他条件检查skip
    # playsound("audio/notification.wav")
    while (True):
        '''
        时间判断 8：am  and 18：pam
        '''

        do_time_period_select()
        do_the_select_and_decision_fast()
        log("等待 " + str(POLL_INTERVAL_IN_SEC / 60) + "min 再次查找")
        time.sleep(POLL_INTERVAL_IN_SEC)
        # do_MA_condition_Analysis("ALICEBUSD","15m")





