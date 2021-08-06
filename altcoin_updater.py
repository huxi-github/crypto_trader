import json
import time
import datetime
from util import send_email,log

from py3commas.request import Py3Commas
from altcoin_ranker import get_top_5_symbol

SCAN_INTERVAL_IN_SEC=60
POLL_INTERVAL_IN_SEC=10#60*15
SCAN_NEW_ARTI_INTERVAL_IN_SEC=10#60*15

p3c = Py3Commas(key='08e94c4768d44f3a9a6f14f68f86a2a63d3dfe67f18c4f28905afad93dfadb92',
                secret='742ce7cffb40f42883e0c454652ebad5d3ccfb125b283b92214401547ea73a'
                       'b2647f42a44e68544054ab9a70769dcfb890fdffe4a181a984287dc8d3e783'
                       'db9a7c501aaacec88af608f0e135f5c2323f921181ea2023176068396eb973'
                       '2c18c487240ec0')


def start_new_deal(coin_pair:str=''):
    response1 = p3c.request(
        entity='bots',
        action='start_new_deal',
            _id="4228101",
        payload={"pair":coin_pair,
                "skip_signal_checks":"true",
                 "skip_open_deals_checks":"true",
                 "bot_id":"4228101"
                 }
    )
    log(response1)
    cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if 'error' not in response1.keys():
        log("\nbots/start_new_deal successfull:")
        send_email(cur_time+" 尝试用交易对"+ coin_pair + "启动DCA机器人成功\n" + "3Commas返回:\n "
                   + json.dumps(response1))
    else:
        log("\nbots/start_new_deal failed:")
        send_email(cur_time+" 尝试用交易对" + coin_pair + "启动DCA机器人失败\n" + "3Commas返回:\n "
                   + json.dumps(response1))

    print("\n")


# PATCH /ver1/bots/{bot_id}/update
# 更新机器人设置
def update_bot_pairs(coin_pair:str='',bot_id:str=''):
    response1 = p3c.request(
        entity='bots',
        action='update',
            _id=bot_id,#"5150456",
        payload={
                 "name" :"Hotest_Coin_15min_Long_Bot1",
                 "pairs":coin_pair,
                 "base_order_volume":150,
                #"base_order_volume_type": "quote_currency",
                 "take_profit":1,
                 "safety_order_volume":120,
                 "martingale_volume_coefficient":1.2,#Safety order volume倍数
                 "martingale_step_coefficient":1,# Safety order间隔倍数
                 "max_safety_orders":16,  #风险意识， 不要 制造不要的灾难>=12
                 "active_safety_orders_count":1,
                 "safety_order_step_percentage":2,
                 "take_profit_type":"total",
                 "strategy_list":"%5B%7B%22strategy%22%3A%22nonstop%22%7D%5D", #manual  nostop==>%5B%7B%22strategy%22%3A%22nonstop%22%7D%5D
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
        log("update_bot_pairs failed:")
        send_email("尝试修改DCA机器人："+bot_id+ "交易对为" + coin_pair + "失败\n" + "3Commas返回:\n "
                   + json.dumps(response1))



##思路1：每天 8 点 定时，创建新的机器人 100 单结束
#思路2：每天 8 点 定时，修改 固定机器人的 交易对信息 为最新交易对
def start():
    # 死循环 ，直到进程结束
    while(True):
        time.sleep(SCAN_INTERVAL_IN_SEC)
        cur_time = datetime.datetime.now().strftime("%H:%M")
        log("current time is " + cur_time)
        if cur_time == "07:00" or cur_time == "08:00":
            log("current time is "+cur_time + "trying to get_top_5_symbol")
            top_symbols =get_top_5_symbol()
            i =0
            for (key,val) in top_symbols.items():
                # print(key+"\t\t\t"+val)
                base = key.replace("BUSD","")
                coin_pair = base+"_BUSD"
                log(coin_pair)
                tv_url = "https://cn.tradingview.com/chart/oLP03YDC/"
                send_email(cur_time + " 今日交易对" + coin_pair+ " 24H 涨幅:"+top_symbols[key]+"%\n"+tv_url)
                start_new_deal(coin_pair)
                i = i + 1
                if i>=2: break


#  策略3每隔  30min/15min 修改一次 机器人参数，交易对修改为最流行的，交易次数修改为15 次， [同时 24H涨幅 >20%的  last_15min>4% last_1h>6% ]
  #策略3 的首单 交易可以设置的比较大， 加仓次数设置 ，为8-10

  #如果3.1 最活跃的币24Hf幅度小于 15%，则发送命令停止该机器人，说明当前整体市场行情下跌
def start_with_poll():
    # 死循环 ，直到进程结束
    while(True):
        time.sleep(POLL_INTERVAL_IN_SEC)
        cur_time = datetime.datetime.now().strftime("%H:%M")
        log("current time is "+cur_time + "trying to get_top_5_symbol")
        top_symbols =get_top_5_symbol()
        i =0
        for (key,val) in top_symbols.items():
            # print(key+"\t\t\t"+val)
            base = key.replace("BUSD","")
            coin_pair = "BUSD_"+base
            tv_url = "https://cn.tradingview.com/chart/oLP03YDC/"
            # send_email(cur_time + " 今日交易对" + coin_pair+ " 24H 涨幅:"+top_symbols[key]+"%\n"+tv_url)
            update_bot_pairs(coin_pair,"5150456")
            i = i + 1
            if i>=2: break

if __name__ == '__main__':
    # start()
    start_with_poll()
    # update_order_account_at_8_am() 每天 1.13% 收益， 复利率 6个月 10 倍！！！！！  【必上 每天选择币重要多了，稳字多么重要】

