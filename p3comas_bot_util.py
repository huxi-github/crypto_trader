# coding: utf-8
from py3commas.request import Py3Commas
from config_5UP_filter import pubkey,secret
from util import send_email,log
import urllib
#账户的 key 和 secr
p3c = Py3Commas(key=pubkey,secret=secret)

def start_a_deal_of_one_bot(coin_pair:str='',bot_id:str=''):
    index_s =coin_pair.find("USDT")
    base = coin_pair[0:index_s]
    symbol_pair = "USDT_"+base
    update_pair_of_huoyue_bot(symbol_pair, bot_id)
    start_the_bot(bot_id)
    start_new_deal(symbol_pair, bot_id)

def start_new_deal(symbol_pair:str="",bot_id:str=''):# from  3commas network
    response1 = p3c.request(
        entity='bots',
        action='start_new_deal',
                _id=bot_id,
        payload={"pair":symbol_pair,
                "skip_signal_checks":"true",
                 "skip_open_deals_checks":"false", #是否跳过界面上的 检查相同交易对并发数目的检查[比较安全]
                 "bot_id":bot_id
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

def start_the_bot(bot_id:str="11358971"):
    response1 = p3c.request(
        entity='bots',
        action='enable',
        _id=bot_id,                   
        payload={"bot_id": bot_id
                 }
    )
    print(response1)
    enabled = response1['is_enabled']
    if enabled:
        print("成功开启机器人:"+bot_id)
        return True
    else:
        print("未能开启机器人:"+bot_id)
        return False

def stop_the_bot(bot_id:str="11358971"):
    response1 = p3c.request(
        entity='bots',
        action='disable',
        _id=bot_id,                   
        payload={"bot_id": bot_id
                 }
    )
    # print(response1)
    disabled = not response1['is_enabled']
    print(response1)
    if disabled:
        print("成功关闭机器人:"+bot_id)
        return True
    else:
        print("未能关闭机器人:"+bot_id)
        return False

# PATCH /ver1/bots/{bot_id}/update
# 更新机器人设置
def update_pair_of_huoyue_bot(coin_pair:str='',bot_id:str='',num:int=0):
    response1 = p3c.request(
        entity='bots',
        action='update',
            _id=bot_id,#"5150456",
        payload={
                 "name" :"Deal_For_Binance_New_Huoyue_Pair"+str(num),
                 "pairs":coin_pair,
                 "base_order_volume":120, #base设置大1000， 目前保守
                 "take_profit":1,  #上线订单，单向行情，TP 大小不影响，可多次小交易
                 "safety_order_volume":100,
                 "martingale_volume_coefficient":1.18,#Safety order volume倍数
                 "martingale_step_coefficient":1,# Safety order间隔倍数
                 "max_safety_orders":7,  #风险意识， (等待到 底部震荡在加仓(自动优化)，成本更低)
                 "active_safety_orders_count":2,
                 "safety_order_step_percentage":2,
                 "take_profit_type":"total",
                 "strategy_list":"%5B%7B%22strategy%22%3A%22nonstop%22%2C%20%22options%22%3A%20%7B%7D%7D%5D", #manual  nostop==>%5B%7B%22strategy%22%3A%22nonstop%22%7D%5D
                 "bot_id":bot_id
                 }
    )
    print(response1)
    # cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if 'error' not in response1.keys():
        log("update_bot+5455831_Hotest_Coin trade_pair to "+ coin_pair + " successfull:" )
        # send_email(cur_time+" 尝试用交易对"+ coin_pair + "启动DCA机器人成功\n" + "3Commas返回:\n "
        #            + json.dumps(response1))   tmp_one_deal_Bot_for_binance_new_parie_on_line#2
    else:
        log("update_bot_pairs failed:")
        # send_email("尝试修改DCA机器人："+bot_id+ "交易对为" + coin_pair + "失败\n" + "3Commas返回:\n "
        #            + json.dumps(response1)) 

# PATCH /ver1/bots/{bot_id}/update
# 更新机器人设置
def update_pair_of_line_bot(coin_pair:str='',bot_id:str='',num:int=0):
    response1 = p3c.request(
        entity='bots',
        action='update',
            _id=bot_id,#"5150456",
        payload={
                 "name" :"One_Deal_For_Binance_New_OnLine_Pair"+str(num),
                 "pairs":coin_pair,
                 "base_order_volume":300, #base设置大1000， 目前保守
                 "take_profit":1,  #上线订单，单向行情，TP 大小不影响，可多次小交易
                 "safety_order_volume":300,
                 "martingale_volume_coefficient":1.18,#Safety order volume倍数
                 "martingale_step_coefficient":1,# Safety order间隔倍数
                 "max_safety_orders":1,  #风险意识， (等待到 底部震荡在加仓(自动优化)，成本更低)
                 "active_safety_orders_count":1,
                 "safety_order_step_percentage":2,
                 "take_profit_type":"total",
                 "strategy_list":"%5B%7B%22strategy%22%3A%22nonstop%22%7D%5D", #manual  nostop==>%5B%7B%22strategy%22%3A%22nonstop%22%7D%5D
                 "bot_id":bot_id
                 }
    )
    print(response1)
    # cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if 'error' not in response1.keys():
        log("update_bot+5455831_Hotest_Coin trade_pair to "+ coin_pair + " successfull:" )
        # send_email(cur_time+" 尝试用交易对"+ coin_pair + "启动DCA机器人成功\n" + "3Commas返回:\n "
        #            + json.dumps(response1)) 	tmp_one_deal_Bot_for_binance_new_parie_on_line#2
    else:
        log("update_bot_pairs failed:")
        # send_email("尝试修改DCA机器人："+bot_id+ "交易对为" + coin_pair + "失败\n" + "3Commas返回:\n "
        #            + json.dumps(response1))

# 更新机器人设置
def set_pairs_of_muti_bot(coin_pair:str='',bot_id:str='',num:int=0):
    response1 = p3c.request(
        entity='bots',
        action='update',
            _id=bot_id,#"5150456",
        payload={
                 "name" :"--------------muti_Pair_test_name",
                 "pairs":coin_pair,
                 "base_order_volume":90, #base设置大1000， 目前保守
                 "take_profit":1,  #上线订单，单向行情，TP 大小不影响，可多次小交易
                 "safety_order_volume":70,
                 "martingale_volume_coefficient":1.18,#Safety order volume倍数
                 "martingale_step_coefficient":1,# Safety order间隔倍数
                 "max_safety_orders":15,  #风险意识， (等待到 底部震荡在加仓(自动优化)，成本更低)
                 "active_safety_orders_count":1,
                 "safety_order_step_percentage":2,
                 "take_profit_type":"total",
                 "strategy_list":"%5B%7B%22strategy%22%3A%22manual%22%7D%5D", #manual  nostop==>%5B%7B%22strategy%22%3A%22nonstop%22%7D%5D
                 "bot_id":bot_id
                 }
    )
    print(response1)
    # cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if 'error' not in response1.keys():
        log("update_bot+5455831_Hotest_Coin trade_pair to "+ coin_pair + " successfull:" )
        # send_email(cur_time+" 尝试用交易对"+ coin_pair + "启动DCA机器人成功\n" + "3Commas返回:\n "
        #            + json.dumps(response1))   tmp_one_deal_Bot_for_binance_new_parie_on_line#2
    else:
        log("update_bot_pairs failed:")
        # send_email("尝试修改DCA机器人："+bot_id+ "交易对为" + coin_pair + "失败\n" + "3Commas返回:\n "
        #            + json.dumps(response1))
def get_symbols():
    symbol_pair_arry=[]
    symbols_file = open("seleted_BUSD[1-13days].txt")
    symbols = symbols_file.readlines()
    for symbol_ in symbols:
        symbol=symbol_.split("BUSD")[0]
        symbol_pair='BUSD'+'_'+symbol
        # print(symbol_pair)
        symbol_pair_arry.append(symbol_pair)
    print(symbol_pair_arry)
    return symbol_pair_arry

def url_encode(in_put:str="$$$"):
    out=urllib.parse.quote(str(in_put),safe='')
    print(out)
    return out



if __name__ == '__main__':
    # symbol_pair_arry=get_symbols()
    # print(symbol_pair_arry_str_encode)
    # test='[{"strategy":"manual"}]'
    # url_encode(test)
    # symbol_pair_arry_url_encode=url_encode(str(symbol_pair_arry))
    # set_pairs_of_muti_bot(symbol_pair_arry_url_encode, "4740610")
    # update_pair_of_huoyue_bot("USDT_BTC", "13779898")
    # start_the_bot("13779898")
    coin_pair="USDT_ETH"
    # start_a_deal_of_one_bot(coin_pair,"13779898")
    start_the_bot("13779898")