from py3commas.request import Py3Commas
from util import log ,send_email
import datetime
import time
from altcoin_updater import POLL_INTERVAL_IN_SEC,SCAN_NEW_ARTI_INTERVAL_IN_SEC



p3c = Py3Commas(key='08e94c4768d44f3a9a6f14f68f86a2a63d3dfe67f18c4f28905afad93dfadb92',
                secret='742ce7cffb40f42883e0c454652ebad5d3ccfb125b283b92214401547ea73a'
                       'b2647f42a44e68544054ab9a70769dcfb890fdffe4a181a984287dc8d3e783'
                       'db9a7c501aaacec88af608f0e135f5c2323f921181ea2023176068396eb973'
                       '2c18c487240ec0')

#////// /ver1/accounts/{account_id}//pie_chart_data
# response1 = p3c.request(
#     entity='accounts',
#     action='pie_chart_data',
#        _id="30227197",
# )
# print("\npie_chart_data:")
# print(response1)

#/////// /ver1/accounts
# response = p3c.request(
#     entity='accounts',
#     action=''
# )
# print("\nlist accounts:")
# print(response)

# ///POST/// /ver1/accounts/{account_id}/account_table_data
# response1 = p3c.request(
#     entity='accounts',
#     action='account_table_data',
#     _id="30227197",
#     payload={"account_id":"30227197"}
# )
# print("\naccount_table_data:")
# print(response1)

#///////GET /ver1/bots/strategy_list
# response1 = p3c.request(
#     entity='bots',
#     action='strategy_list',
#     param ="account_id=30227197&type=simple&strategy=long"
# )
# print("\nbots/strategy_list:")
# print(response1)

# ///////GET /ver1/bots

# response1 = p3c.request(
#     entity='bots',
#     action=''
# )
# print("\nlist all bots info:")
# print(response1)


# ///////GET /ver1/bots/stats  单个机器人收益统计

# response1 = p3c.request(
#     entity='bots',
#     action='stats',
#     param ="account_id=30227197&bot_id=4228101" #
# )
# print("\nbots/stats:")
# print(response1)

# /////// POST /ver1/bots/{bot_id}/disable
# response1 = p3c.request(
#     entity='bots',
#     action='enable',
#         _id="4228101",
#     payload={
#              "bot_id":"4228101"
#              }
# )

# ///////POST /ver1/bots/{bot_id}/start_new_deal  [仅仅对 muti-pair 机器人使用这个接口 可用]

def start_new_deal():
    response1 = p3c.request(
        entity='bots',
        action='start_new_deal',
            _id="4228101",
        payload={"pair":"USDT_BTC",
                "skip_signal_checks":"true",
                 "skip_open_deals_checks":"true",
                 "bot_id":"4228101"
                 }
    )
    print(response1)
    if 'error:' not in response1:
        print("\nbots/start_new_deal successfull:")
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
        if symbl_d['symbol'].endswith("BUSD") :
            if "BULL" in symbl_d['symbol'] or "DOWN" in symbl_d['symbol']: continue
            print(str(i)+ "\t\t" + symbl_d['symbol'] + "\t\t\t\t\t" + symbl_d['priceChangePercent'])
            i = i + 1
            top_hot_symbol[symbl_d['symbol']]=symbl_d['priceChangePercent']
            if i>=5: break
    return top_hot_symbol

def get_fast_change_coin():
    top_symbols = get_top_coin()
    i = 0
    for (key, val) in top_symbols.items():
        coin_pair = key
        tv_url = "https://cn.tradingview.com/chart/oLP03YDC/"
        # send_email(cur_time + " 今日交易对" + coin_pair+ " 24H 涨幅:"+top_symbols[key]+"%\n"+tv_url)
        # update_bot_pairs(coin_pair, "5150456")
        # i = i + 1
        # if i >= 2: break
        re = get_coin_stat(coin_pair,"5m",12)
        print(coin_pair + "is fast coin? re="+str(re))

def get_fast_change_coin_1m():
    top_symbols = get_top_coin()
    i = 0
    for (key, val) in top_symbols.items():
        coin_pair = key
        tv_url = "https://cn.tradingview.com/chart/oLP03YDC/"
        # send_email(cur_time + " 今日交易对" + coin_pair+ " 24H 涨幅:"+top_symbols[key]+"%\n"+tv_url)
        # update_bot_pairs(coin_pair, "5150456")
        # i = i + 1
        # if i >= 2: break
        re = get_coin_stat(coin_pair,"1m",60)
        print(coin_pair + "is fast coin? re="+str(re))

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
    if sustain_n>limit/3:
        return True
    else:
        return False


# ///////GET /api/v3/klines
def get_symbol_change_of_last_frame(symbol:str="",watch_interval:str="5m"):
    limit =1
    params_str= "symbol="+symbol+"&interval="+watch_interval+"&limit="+str(limit)
    data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/klines",
            params=params_str   # params="symbol=C98USDT&interval=5m&limit=3"         #一个符号
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
    print("交易对"+symbol+" 在最近"+str(limit)+" 个"+watch_interval+"内变化:"+ str(price_change_percent)[:4] +"%"+"\t振幅变化:" + str(price_change_max_percent)[:4] +"%")
    return price_change_percent

def get_symbol_change_rank_of_frame(watch_interval:str="15m"):
    top_symbols = get_top_coin()
    symbol_arr={}
    for (key, val) in top_symbols.items():
        coin_pair = key
        price_change_percent = get_symbol_change_of_last_frame(coin_pair,watch_interval)
        symbol_arr[coin_pair] = price_change_percent
    sorted_arry = sorted(symbol_arr.items(), key = lambda i: float(i[1]),reverse = True)
    # print(sorted_arry)
    print("TOP5 "+watch_interval+"内变化榜:")
    for (key, val) in sorted_arry:
        print(key +"   "+str(val)[:4]+"%")
        # if(val>5):
        if (val>6):
            print("涨幅榜top5的交易对" + key + " 在最近"+ watch_interval
                  + "内拉升超5% ，实际幅度为:" + str(val)[:4] + "%")
            send_email("涨幅榜top5的交易对" + key + " 在最近"+ watch_interval
                  + "量化区间内砸盘超5% ，实际幅度为:" + str(val)[:4] + "%"
                       +"收到推送后现在 tradingview 上观察 模拟一两天，几次之后再实盘 稳重的话，一个符号一单，再换其他pump symbol"
                       +"1.观察1.TV 1h量化图，处于 上升期 还是 下跌期 \n 2.24H 涨幅  \n3.单日大盘行情 \n4."
                        "回调距离成本线距离，SO的大小>4 目前模拟结果，问题较大\n"
                        "查看实时模拟:https://cn.tradingview.com/chart/oLP03YDC/?symbol=BINANCE%3A"+key)


# PATCH /ver1/bots/{bot_id}/update
#3 每隔  30min/15min 修改一次 机器人参数，交易对修改为最流行的  ，交易次数修改为15 次(error no)， [同时 24H涨幅 >20%的  last_15min>4% last_1h>6% ]
  #策略3 的首单 交易可以设置的比较大， 加仓次数设置 ，为8-10
  # 5min 级别更新一次，跟新为 5min 连续上涨， 连续5min 上涨 ， 1min 变化幅度>2.5%
def update_bot_pairs(coin_pair:str='',bot_id:str=''):
    response1 = p3c.request(
        entity='bots',
        action='update',
            _id=bot_id,#"5150456",
        payload={
                 "name" :"Hotest_Coin_15min_Long_Bot1",
                 "pairs":coin_pair,
                 "base_order_volume":150,
                        # "base_order_volume_type": "quote_currency",
                 "take_profit":1,
                 "safety_order_volume":120,
                 "martingale_volume_coefficient":1.2,#Safety order volume倍数
                 "martingale_step_coefficient":1,# Safety order间隔倍数
                 "max_safety_orders":10,
                 "active_safety_orders_count":1,
                 "safety_order_step_percentage":2,
                 "take_profit_type":"total",
                 "strategy_list":"%5B%7B%22strategy%22%3A%22manual%22%7D%5D", #manual  nostop==>%5B%7B%22strategy%22%3A%22nonstop%22%7D%5D
                 "bot_id":bot_id
                 }
    )
    # log(json.dumps(response1))
    # cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if 'error' not in response1.keys():
        log("update_bot 5150456_Hotest_Coin trade_pair to "+ coin_pair + " successfull:" )
        # send_email(cur_time+" 尝试用交易对"+ coin_pair + "启动DCA机器人成功\n" + "3Commas返回:\n "
        #            + json.dumps(response1))
    else:
        log("bots/update_bot_pairs failed:")
        # send_email(cur_time+" 尝试用交易对" + coin_pair + "启动DCA机器人失败\n" + "3Commas返回:\n "
        #            + json.dumps(response1))

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


if __name__ == '__main__':

    # get_top_coin()
    # start_new_deal()
    # update_bot_pairs("USDT_BTC","5150456")

    # get_fast_change_coin()  # 思路，，，前10名 里面进进行筛选
    # get_fast_change_coin_1m()
    # get_symbol_change_of_last_frame("ALICEBUSD","15m")
    # re = get_coin_static("HEGICBUSD", "3m", 20)


#-----15 min 拉盘警告
    while(True):
        cur_time = datetime.datetime.now().strftime("%H:%M")
        log("current time is "+cur_time + "trying to get_top_5_symbol")
        get_symbol_change_rank_of_frame("15m")
        time.sleep(POLL_INTERVAL_IN_SEC)

#------上市通知警告
    # while(True):
    #     get_anooucement_1h()
    #     time.sleep(SCAN_NEW_ARTI_INTERVAL_IN_SEC)
    # 交易所 大挂单 分析==>辅助压力线，//////




