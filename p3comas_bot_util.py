# coding: utf-8
from py3commas.request import Py3Commas
from util import send_email,log
import urllib

p3c = Py3Commas(key='xx',
                secret='xx'
                       ' '
                       ' '
                       ' ')
# PATCH /ver1/bots/{bot_id}/update
# 更新机器人设置
def update_pair_of_line_bot(coin_pair:str='',bot_id:str='',num:int=0):
    response1 = p3c.request(
        entity='bots',
        action='update',
            _id=bot_id,#"5150456",
        payload={
                 "name" :"One_Deal_For_Binance_New_Online_Pair"+str(num),
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
                 "strategy_list":"%5B%7B%22strategy%22%3A%22manual%22%7D%5D", #manual  nostop==>%5B%7B%22strategy%22%3A%22nonstop%22%7D%5D
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
    symbol_pair_arry=get_symbols()
    # print(symbol_pair_arry_str_encode)
    # test='[{"strategy":"manual"}]'
    # url_encode(test)
    symbol_pair_arry_url_encode=url_encode(str(symbol_pair_arry))
    set_pairs_of_muti_bot(symbol_pair_arry_url_encode, "4740610")
        # update_pair_of_line_bot("BUSD_BTC", "5455831")