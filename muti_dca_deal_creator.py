from py3commas.request import Py3Commas
from util import log ,send_email
import datetime
import time

POLL_INTERVAL_IN_SEC =3
SCAN_NEW_ARTI_INTERVAL_IN_SEC =60*5
#模拟账户的 key 和 secr
p3c = Py3Commas(key='369e09cb3e034f7e9627cda9c0a74a1310ab3a8f45e6425fb80b574ec88726b3',
                secret='4fea99fcd0f8f4b39c51c1ac360481b4179e5f58fc67686ecfa0f9bd1affec9aeeb282ddfd5da63bdd0c74a8239c1d5d99cc9f884aca85e84fcb5c4a48295885f796da40127764a2191d42e65581ca406abbd193ba1259abdb1cb16d265e93963f0e74b9')

# ///////POST /ver1/bots/{bot_id}/start_new_deal  [仅仅对 muti-pair 机器人使用这个接口 可用]
def start_new_deal(coin_pair:str=""):# from  3commas network
    index_s =coin_pair.find("USDT")
    base = coin_pair[0:index_s]
    symbol_pair = "USDT_"+base

    response1 = p3c.request(
        entity='bots',
        action='start_new_deal',
            # _id="4228101",
                _id="11358971",
        payload={"pair":symbol_pair,
                "skip_signal_checks":"true",
                 "skip_open_deals_checks":"false", #是否跳过界面上的 检查相同交易对并发数目的检查[比较安全]
                 "bot_id":"11358971"
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

def start_new_deal_real(coin_pair:str=""):# from  3commas network
    index_s =coin_pair.find("USDT")
    base = coin_pair[0:index_s]
    symbol_pair = "USDT_"+base

    response1 = p3c.request(
        entity='bots',
        action='start_new_deal',
            # _id="4228101",
                _id="11367606",
        payload={"pair":symbol_pair,
                "skip_signal_checks":"true",
                 "skip_open_deals_checks":"false", #是否跳过界面上的 检查相同交易对并发数目的检查[比较安全]
                 "bot_id":"11367606"
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
    i=0
    sorted_arry = sorted(data_arry, key = lambda i: float(i['priceChangePercent']),reverse = True)
    print("24H 涨幅榜前5:")
    print('rank"\tsymbol_name ' + "\t\t\t" + 'priceChangePercent')
    top_hot_symbol={}
    for symbl_d in sorted_arry:
        if symbl_d['symbol'].endswith("USDT") :
            if "BULL" in symbl_d['symbol'] or "DOWN" in symbl_d['symbol']: continue
            print(str(i)+ "\t\t" + symbl_d['symbol'] + "\t\t\t\t\t" + symbl_d['priceChangePercent'])
            i = i + 1
            top_hot_symbol[symbl_d['symbol']]=symbl_d['priceChangePercent']
            if i>=15: break
    return top_hot_symbol


# ///////GET /api/v3/klines
def get_symbol_change_of_last_frame(symbol:str="",watch_interval:str="5m"):
    data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/klines",
            params="symbol="+symbol+"&interval="+watch_interval+"&limit="+str(1)
            )
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

def start_just_one_deal_of_pair_muti_bot(coin_pair:str=""):
    print("开启mutil-pair-bot 一单，交易对:" + coin_pair)
    # sprint("开启mutil-pair-bot 一单，交易对:" + coin_pair)
    # log_deal_to_log_file_with_time()
    start_new_deal(coin_pair)
    # ////// 打印该币 是否支持杠杆---


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
    log("current time is " + cur_time + "trying to get_top_5_symbol")
    top_symbols = get_top_coin()

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
                if price_change_1m > 0.1 and price_change_1m < 10: #(<10% 反向插针，诱高的情况)
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


if __name__ == '__main__':
    # #-----15 min 拉盘启动模拟账户交易
    # [new deal 条件 1.15min 6%up  2.10min 2%up （3)3min 1.5%  (4)1min 1% up]  （5）信号其他条件检查skip
    while (True):
        '''
        时间判断 8：am  and 18：pam
        '''
        # do_time_period_select()
        do_the_select_and_decision_fast()
        log("等待 " + str(POLL_INTERVAL_IN_SEC / 60) + "min 再次查找")
        time.sleep(POLL_INTERVAL_IN_SEC)





