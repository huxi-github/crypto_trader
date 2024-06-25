

from py3commas.request import Py3Commas
from util import log, send_email, read_news_title_with_speaker, log_to_file,SMA
import datetime
import time
from config import *
import json

POLL_INTERVAL_IN_SEC =3
SCAN_NEW_ARTI_INTERVAL_IN_SEC =60*5
#账户的 key 和 secr
p3c = Py3Commas(key=pubkey,secret=secret)

def start_new_deal(coin_pair:str="",allow_same_pair:bool=False):# from  3commas network
    index_s =coin_pair.find("BUSD")
    base = coin_pair[0:index_s]
    symbol_pair = "BUSD_"+base
    skip_same_deals_checks=allow_same_pair
    response1 = p3c.request(
        entity='bots',
        action='start_new_deal',
            _id="4228101", #虚拟账户
            # _id="4740610", #真实账户 机器人
        payload={"pair":symbol_pair,
                "skip_signal_checks":"false",#trading 15min  推荐买入，检查
                 "skip_open_deals_checks":skip_same_deals_checks, #是否跳过界面上的 同时相同交易对数目的检查[比较安全]
                 "bot_id":"4228101"  # 虚拟账户
                 # "bot_id":"4740610"  #真实账户 机器人
                 }
    )

    print("服务器返回+resp_txt===="+str(response1))# from  3commas network网络回复
    if 'error:' in response1:
        print("\nbots/start_new_deal failed:"+"symbol_pair="+symbol_pair)
        print("\n请求的参数可能存在错误")
    elif 'rejected-max-deal' in response1: #自己定义rejected
        cur_time = datetime.datetime.now().strftime("%m-%d %H:%M:%S")
        print("\n达到最大订单数限制 for" + " symbol_pair=" + symbol_pair+"暂停20s再扫描......")
        send_email(cur_time+"达到最大订单数限制 for" + " symbol_pair=" + symbol_pair+"暂停20s再扫描......")
        time.sleep(20)
    elif 'rejected-not-exsit' in response1: #自己定义rejected
        print("\n交易对不再交易对备选表中 for" + " symbol_pair=" + symbol_pair+"跳过，扫描下一个")
        send_email("\n交易对不再交易对备选表中 for" + " symbol_pair=" + symbol_pair+"跳过，扫描下一个")
    elif 'net_timeout' in response1:
        print("\n3commas.io网络拥塞，已经尝试5次连接(2.3) for" + " symbol_pair=" + symbol_pair + "不等待 3s，之后进入下一轮扫描，直接扫")
        send_email("\n3commas.io网络拥塞4X(2.3)s for" + " symbol_pair=" + symbol_pair + "不等待,直接扫下一轮,币安扫描要时间")
    else:
        print("\nbots/start_new_deal successful 成功:"+"symbol_pair="+symbol_pair)
    print("\n")

# ///////GET /api/v3/ticker/24hr
def get_top_coin():
    data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/ticker/24hr"
            )
    if 'net_erro' in data_arry:
        net_erro_inf = data_arry
        log_to_file("get_top_coin failed pass，返回"+str(net_erro_inf),'net_erro_test_api')
        return net_erro_inf

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
            if i>=TOP_COIN_SCAN_NUM: break
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
    if 'net_erro' in data_arry:
        net_erro_inf = data_arry
        log_to_file("get_top_coin failed pass，返回"+str(net_erro_inf),'net_erro_test_api')
        return net_erro_inf
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
    if sustain_n>limit/3:
        return True
    else:
        return False


# ///////GET /api/v3/klines
def get_symbol_change_of_last_frame(symbol:str="",watch_interval:str="5m"):
    data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/klines",
            params="symbol="+symbol+"&interval="+watch_interval+"&limit="+str(1)
            )

    if 'net_erro' in data_arry:
        log_to_file("get_symbol_change_of_last_frame failed pass，范围变化幅度-1(%)", 'net_erro_test_api')
        return -1
    data = data_arry[-1] #[-1]是最后一根bar
    open = float(data[1])
    high = float(data[2])
    low  = float(data[3])
    close= float(data[4]) # close==cur_price
    price_change_max_percent = 100.00*(high-low)/open
    price_change_percent= 100.00*(close-open)/open
    print("open:"+str(open))
    print("close:" + str(close))#close即是 当前价格
    print("交易对"+symbol+" 在最近1个"+watch_interval+"内变化:"+ str(price_change_percent)[:4] +"%"
                                                +"\t振幅变化:" + str(price_change_max_percent)[:4] +"%")
    return price_change_percent


# /// / ///GET /api/v3/klines
def check_is_near_fibonacci_price_of_TODAY(symbol:str=""):
    limit:str = '7'
    watch_interval:str = "1d"
    data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/klines",
            params="symbol="+symbol+"&interval="+watch_interval+"&limit="+limit
            )
    if 'net_erro' in data_arry:
        log_to_file("get_symbol_MA_of_last_frame_s failed，返回-1",'net_erro_test_api')
        return -1
    data =data_arry[-1] # json 是按照时间序列排列的 [-1] [-1] 是最后一个元素，即最近一天
    symbl_d = data
    open = float(symbl_d[1]) #
    high = float(symbl_d[2]) #当天最高价
    low = float(symbl_d[3])
    close = float(symbl_d[4])#close即是 当前价格cur_price]
    cur = close

    if cur<open:
        print("day_cur=" + str(cur)+" day_open="+str(open))

        print("当日价格小于开盘价")
        # read_news_title_with_speaker("当天行情是 负值，不入场")
        return True

    limit:str = str(int(24*60/15))#'#str(int(24*60/15))  /24h
    watch_interval:str = "15m"  #时间更新 精度 15min
    data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/klines",
            params="symbol="+symbol+"&interval="+watch_interval+"&limit="+limit
            )
    if 'net_erro' in data_arry:
        log_to_file("get_symbol_MA_of_last_frame_s failed，返回-1",'net_erro_test_api')
        return -1

    for i in range(0,len(data_arry)):
        data = data_arry[i]
        close_t = float(data[4])
 

    high_24h=0 #每小时更新一次,24h 分段计算更新最高点  (96*15min 15min 分批更新图)
    high_24h_stamp=0
    data_arry.pop()  #去除一个当前小时的
    length=len(data_arry)
    high_index=0
    for i in range(0,length):
        data = data_arry[i]
        high_t = float(data[2])
        stamp_t = float(data[6])/1000 #化成标准10位时间
        if high_t>high_24h:
            high_24h=high_t  # high_last_24h
            high_24h_stamp=stamp_t
            high_index=i

    lowest_mid=high_24h
    lowest_mid_stamp=0
    lowest_mid_index=0
    for i in range(high_index,length):
        data = data_arry[i]
        low_t = float(data[3])
        stamp_t = float(data[6])/1000 #化成标准10位时间
        if low_t<lowest_mid:
            lowest_mid=low_t  # high_last_24h
            lowest_mid_stamp=stamp_t
            lowest_mid_index=i

    cur_stamp=time.time()
    LT=(lowest_mid_stamp-high_24h_stamp)/60
    RT=(cur_stamp-lowest_mid_stamp)/60

    print("low_middle_index="+str(lowest_mid_index))
    # position = (high - cur) / (high - open)
    position = (high_24h - cur) / (high_24h - open)
    print("high_24h=" + str(high_24h) + "lowest_mid="+str(lowest_mid)+" cur=" + str(cur)+" open="+str(open))

    print("high_24h_stamp="   + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(high_24h_stamp))))
    print("lowest_mid_stamp=" + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(lowest_mid_stamp))))
    print("cur_stamp="        + str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(cur_stamp))))
    day = datetime.datetime.now().strftime("%Y-%m-%d")
    cur_from_day_high_in_mins = int((cur_stamp - high_24h_stamp)/60)

    if cur_from_day_high_in_mins <=15: #15min
        if 0 < position and position < 0.236:
            # read_news_title_with_speaker("最高点后的0-15分钟,进入斐波区间")#回落
            log_to_file("最高点后的0-15分钟,进入斐波区间 ", "trigered_pair/pairs_" + day + ".log")
            return False
        if -0.1 < position and position <= 0:
            # read_news_title_with_speaker("最高点后的0-15分钟，持续爆拉升突破前高...")
            log_to_file("最高点后的0-15分钟，持续爆拉升突破前高... ", "trigered_pair/pairs_" + day + ".log")
            return False
        if position<-0.1:
            # read_news_title_with_speaker("最高点后的0-15分钟，持续爆拉升突破前高10%...")
            log_to_file("最高点后的0-15分钟，持续爆拉升突破前高10%...", "trigered_pair/pairs_" + day + ".log")
            log_to_file("high_24h=" + str(high_24h) + " cur=" + str(cur), "trigered_pair/pairs_" + day + ".log")
            return False
        if position>0.236:
            # read_news_title_with_speaker("最高点后的0-15分钟，进入斐波区间下面的拉升")
            log_to_file("最高点后的0-15分钟，进入斐波区间下面的拉升 ", "trigered_pair/pairs_" + day + ".log")
            log_to_file("high_24h=" + str(high_24h) + " cur=" + str(cur), "trigered_pair/pairs_" + day + ".log")
            return False
    elif 15 <cur_from_day_high_in_mins and cur_from_day_high_in_mins <=45: #45min
        if 0 < position and position < 0.236:
            # read_news_title_with_speaker("最高点后的15-45分钟 ， 进入斐波区间")
            log_to_file("最高点后的15-45分钟 ， 跌落后进入斐波区间 ", "trigered_pair/pairs_" + day + ".log")
            return True
        if -0.1 < position and position <= 0:
            # read_news_title_with_speaker("最高点后的15-45分钟 ，拉升突破前高...")
            log_to_file("最高点后的15-45分钟 ，拉升突破前高...", "trigered_pair/pairs_" + day + ".log")
            return True
        if position<-0.1:
            # read_news_title_with_speaker("最高点后的15-45分钟，拉升突破前高10%...")
            log_to_file("最高点后的15-45分钟，拉升突破前高10%... ", "trigered_pair/pairs_" + day + ".log")
            log_to_file("high_24h=" + str(high_24h) + " cur=" + str(cur), "trigered_pair/pairs_" + day + ".log")
            return False
        if position>0.236:
            # read_news_title_with_speaker("最高点后的15-45分钟，再次进入斐波区间前的拉升")
            log_to_file("高点后的15-45分钟，再次进入斐波区间前的拉升 ", "trigered_pair/pairs_" + day + ".log")
            log_to_file("high_24h=" + str(high_24h) + " cur=" + str(cur), "trigered_pair/pairs_" + day + ".log")
            return False
    elif 45 <cur_from_day_high_in_mins and cur_from_day_high_in_mins : #45min
        log_to_file("最高点后的"+str(cur_from_day_high_in_mins)[0:4]+"分钟， 拉升  ", "trigered_pair/pairs_" + day + ".log")
        log_to_file("LeftTime="+str(LT)[0:4]+"分钟，RightTime="+str(RT)[0:4]+"分钟", "trigered_pair/pairs_" + day + ".log")
        log_to_file("左右时间比为: "+str(LT/RT)+"比1", "trigered_pair/pairs_" + day + ".log")
        # read_news_title_with_speaker("左右时间比为: "+str(int(LT/RT))+"比1,距离上次高点:"+readable_time(cur_from_day_high_in_mins))

        if LT/RT>1.5 or LT<30 :
            # read_news_title_with_speaker("判断为下跌趋势临时回弹，放弃")
            return True

        if 0 < position and position < 0.236:
            # read_news_title_with_speaker("最高点后的45分钟之后， 大低谷回落 再次 进入斐波区间")
            log_to_file("最高点后的45分钟之后， 大低谷回落 再次 进入斐波区间 ", "trigered_pair/pairs_" + day + ".log")
            return True
        if -0.1 < position and position <= 0:
            # read_news_title_with_speaker("最高点后的45 分钟之后，短期持续爆拉升突破前高...")
            log_to_file("最高点后的45 分钟之后，短期持续爆拉升突破前高... ", "trigered_pair/pairs_" + day + ".log")
            return True
        if  position<-0.1:
            # read_news_title_with_speaker("最高点后的45 分钟之后，持续爆拉升突破前高10%...")
            log_to_file("最高点后的45 分钟之后，持续爆拉升突破前高10%... ", "trigered_pair/pairs_" + day + ".log")
            log_to_file("high_24h=" + str(high_24h) + " cur=" + str(cur), "trigered_pair/pairs_" + day + ".log")
            return False
        if position>0.236:
            # read_news_title_with_speaker("最高点后的45 分钟之后，斐波区间下面的拉升")
            log_to_file("最高点后的45 分钟之后，斐波区间下面的拉升", "trigered_pair/pairs_" + day + ".log")
            log_to_file("high_24h=" + str(high_24h) + " cur=" + str(cur), "trigered_pair/pairs_" + day + ".log")
            return False


def readable_time(time_in_mins:int=0):
    print("time_in_mins="+str(time_in_mins))
    if time_in_mins<60:
        return str(time_in_mins)+"分钟"
    elif 60<=time_in_mins and time_in_mins<60*24:
        hours= int(time_in_mins/60)
        min_left= time_in_mins%60
        return str(hours)+"小时"+str(min_left)+"分钟"
    elif 60*24<=time_in_mins and time_in_mins<60*24*7:
        days= int(time_in_mins/(60*24))
        print(days)
        hours=int(time_in_mins%(60*24)/60)
        mins= int(time_in_mins%(60*24)%60)
        # return str(days)+"天"+str(hours)+"小时"+str(mins)+"分钟"  
        return str(days)+"天"+str(hours)+"小时"     #天级别忽略分钟
    else:
        weeks= int(time_in_mins/(60*24*7))
        days=  int(time_in_mins%(60*24*7)/(60*24))
        hours= int(time_in_mins%(60*24*7)%(60*24)/60)
        mins=  int(time_in_mins%(60*24*7)%(60*24)%60)
        # return str(weeks)+"周"+str(days)+"天"+str(hours)+"小时"+str(mins)+"分钟"
        return str(weeks)+"星期"+str(days)+"天"+str(hours)+"小时" #周级别忽略分钟






    '''
#################--------------###################
    if 0<position and position<0.236:         #1.非波那契回撤   （具体参数 pine tv 回测）
        last_min = (cur_stamp - high_24h_stamp) / 60
        if last_min <15:  # 1.1 拉升过程临时 回落进入斐波区间)
            read_news_title_with_speaker("拉升15min后临时 回落进入斐波区间")
            log_to_file("拉升5min后临时 回落进入斐波区间... ", "trigered_pair/pairs_" + day + ".log")
            return False
        if 15<last_min and last_min<45:    #1.2回落进入)
            read_news_title_with_speaker("拉升高点15-45min后， 临时 回落进入斐波区间")
            log_to_file("价格拉升高点5-15min后， 临时 回落进入斐波区间 ", "trigered_pair/pairs_" + day + ".log")
            log_to_file("high_24h="+str(high_24h)+" cur="+str(cur),"trigered_pair/pairs_" + day + ".log")
            return True
        if last_min>=45:    #1.3  45min后回落进入斐波区间)
            read_news_title_with_speaker("拉升后45min后，进入斐波区间")
            log_to_file("价格拉升后45min后，进入斐波区间 ", "trigered_pair/pairs_" + day + ".log")
            log_to_file("high_24h="+str(high_24h)+" cur="+str(cur),"trigered_pair/pairs_" + day + ".log")
            return True
    elif -0.1<position and position<=0:       #2.突破波那区间 判断
        last_min=(cur_stamp-high_24h_stamp)/60
        if last_min<15:       #2.1持续拉升突破
            read_news_title_with_speaker("短期持续爆拉升突破前高...")
            log_to_file("价格短期持续爆拉升突破前高... ", "trigered_pair/pairs_" + day + ".log")
            return False
        if last_min>=15:    #2.2回落突破)
            print("进入 至假突破判定区间，不入场")
            read_news_title_with_speaker("进入 假突破区间，不入场")
            log_to_file("价格假突破区间，不入场 ", "trigered_pair/pairs_" + day + ".log")
            return True
    elif position<-0.1:                      #3 突破前高0.1倍->冲破 10% of 单日区间
        read_news_title_with_speaker("突破假突破 限制区间，入场")
        log_to_file("价格 突破 假突破判定区间，入场","trigered_pair/pairs_" + day + ".log")
        return False
    else:          #4 position>0.236 未上升至 波切区间
        log_to_file("未进入 波切区间... ","trigered_pair/pairs_" + day + ".log")
        return False
 还未测试
        #4.2 由状态1回落至斐波那切区间下面 (可以不管/？)
        data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/klines",
            params="symbol=" + symbol + "&interval=" + "5m" + "&limit=1"
        )
        data = data_arry[-1]
        _5min_high=data[2]
        pos=(high_24h - _5min_high) / (high_24h - open)
        if pos<0.236:  #5min 前从斐波区间回落
            return True
'''

# ///////GET /api/v3/klines
def get_symbol_MA_of_last_frame_s(symbol:str="",watch_interval:str="5m",limit:str='0'):
    data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/klines",
            params="symbol="+symbol+"&interval="+watch_interval+"&limit="+limit
            )
    if 'net_erro' in data_arry:
        log_to_file("get_symbol_MA_of_last_frame_s failed，返回-1",'net_erro_test_api')
        return -1
    close_sum =0.0
    for data in data_arry:
        symbl_d = data
        close= float(symbl_d[4])
        close_sum = close_sum+close
    close_ave=close_sum/float(limit)
    #close即是 当前价格
    print("交易对"+symbol+" 在最近"+str(limit)+"个"+watch_interval+" MA"+limit+":="+str(close_ave))
    return close_ave


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




def  start_just_one_deal_of_pair_muti_bot(coin_pair:str=""):
    # print("砸盘超6% ，实际幅度为:" + str(val)[:4] + "%"
    #            +"收到推送后现在 tradingview 上观察 模拟一两天，几次之后再实盘 稳重的话，一个符号一单，再换其他pump symbol"
    #            +"1.观察1.TV 1h量化图，处于 上升期 还是 下跌期 \n 2.24H 涨幅  \n3.单日大盘行情 \n4."
    #             "回调距离成本线距离，SO的大小>4 目前模拟结果，问题较大\n"
    #             "查看实时模拟:https://cn.tradingview.com/chart/oLP03YDC/?symbol=BINANCE%3A"+key)

    print("开启mutil-pair-bot 一单，交易对:" + coin_pair)
    read_news_title_with_speaker("开启DCA交易单，交易对:" + str(coin_pair))
    day = datetime.datetime.now().strftime("%Y-%m-%d")
    log_to_file(coin_pair+" trigerd","trigered_pair/pairs_"+day+".log")
                                                        # price_change_10m = get_symbol_change_of_last_frame_s(coin_pair, "5m",'2')#10min级别 检查
    # re=check_is_near_fibonacci_price_of_TODAY(coin_pair)
    # if re:
    #     read_news_title_with_speaker(coin_pair +"判定为菲波那切区间内,放弃") #菲波那切区间 包含假突破
    #     return
    start_new_deal(coin_pair)
    # log("模拟账户同时创建订单"+coin_pair)
    # start_new_deal_test_account(coin_pair)

    # MA_OK=do_MA_condition_Analysis(coin_pair,"15m")
    # if not  MA_OK:
    #     index_s = coin_pair.find("BUSD")
    #     base = list(coin_pair[0:index_s])
    #     send_email("货币【_" + str(base) + "】符合3个条件,不符合15分钟MA条件，交易放弃")
    #     # read_news_title_with_speaker("货币【_" + str(base) + "】符合3个条件,但不符合15分钟M A条件，交易放弃")
    #     return


    # ////// 打印该币 是否支持杠杆---
    # playsou nd("notification.wav")
    # index_s = coin_pair.find("BUSD")
    # base = list(coin_pair[0:index_s])
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
    if 'net_erro' in top_symbols:
        log_to_file("get_top_coin failed pass,跳过等待下次扫描",)
        return {"net_erro":"网络故障"}

    sel = []
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
        if price_change_15m > 2.5 and price_change_15m < 50:#(<50%排除新币上线的单当 天情况，新上线的新币不会再 备选表里面，)
            price_change_5m = get_symbol_change_of_last_frame(coin_pair, "5m")
            if  price_change_5m > 1.5  :
                price_change_1m = get_symbol_change_of_last_frame(coin_pair, "1m")
                if price_change_1m > 0.1 and price_change_1m < 3: #(<5% 反向插针，诱高的情况)
                    sel.append(coin_pair)
                    print("交易对【"+coin_pair+"】符合3个条件，直接启动交易")
                    start_just_one_deal_of_pair_muti_bot(coin_pair)  # 仅仅参与一单
                    # print("交易对【" + coin_pair + "】符合3个条件，直接启动交易")===>开启的交易对放在一个log 里面
                else:
                    print("1min涨幅不符合条件")
            else:
                print("5min涨幅不符合条件")
        else:
            print("15min涨幅不符合条件")

    print("本符合条件，启动的的交易符号："+str(sel))

def do_time_period_select():
    # BTC_PRC>STOP_RUNNING_PRIC
    # exit(0)
    pass



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
    #     get_anooucement_1h()
    #     time.sleep(SCAN_NEW_ARTI_INTERVAL_IN_SEC)
    # 交易所 大挂单 分析==>辅助压力线，//////



if __name__ == '__main__':
    #-----15 min 拉盘启动模拟账户交易
    # [new deal 条件 1.15min 6%up  2.10min 2%up （3)3min 1.5%  (4)1min 1% up]  （5）信号其他条件检查skip
    re = check_is_near_fibonacci_price_of_TODAY("GALABUSD")
    print(re)
    # if not re:
    #     start_new_deal("GALABUSD")
    # print(time.time())

    # print(readable_time(60*24*7+60*28+1))

    while (True):
        '''
        时间判断 8：am  and 18：pam
        1.BTC 设定的阻力位价格
        2.BTC 大盘当天行情
        '''
        # read_news_title_with_speaker("时间判断")
        do_time_period_select()
        do_the_select_and_decision_fast()
        log("等待 " + str(POLL_INTERVAL_IN_SEC / 60) + "min 再次查找")
        time.sleep(POLL_INTERVAL_IN_SEC)







