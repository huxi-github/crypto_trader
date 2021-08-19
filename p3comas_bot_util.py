# coding: utf-8
from py3commas.request import Py3Commas
from util import send_email,log

p3c = Py3Commas(key='08e94c4768d44f3a9a6f14f68f86a2a63d3dfe67f18c4f28905afad93dfadb92',
                secret='742ce7cffb40f42883e0c454652ebad5d3ccfb125b283b92214401547ea73a'
                       'b2647f42a44e68544054ab9a70769dcfb890fdffe4a181a984287dc8d3e783'
                       'db9a7c501aaacec88af608f0e135f5c2323f921181ea2023176068396eb973'
                       '2c18c487240ec0')
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
                 "base_order_volume":1500,
                 "take_profit":7,  #上线订单 TP 可设置大些
                 "safety_order_volume":1000,
                 "martingale_volume_coefficient":1.18,#Safety order volume倍数
                 "martingale_step_coefficient":1,# Safety order间隔倍数
                 "max_safety_orders":10,  #风险意识， 不要 制造不要的灾难>=12
                 "active_safety_orders_count":1,
                 "safety_order_step_percentage":2,
                 "take_profit_type":"total",
                 "strategy_list":"%5B%7B%22strategy%22%3A%22manual%22%7D%5D", #manual  nostop==>%5B%7B%22strategy%22%3A%22nonstop%22%7D%5D
                 "bot_id":bot_id
                 }
    )
    # cur_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if 'error' not in response1.keys():
        log("update_bot+5455831_Hotest_Coin trade_pair to "+ coin_pair + " successfull:" )
        # send_email(cur_time+" 尝试用交易对"+ coin_pair + "启动DCA机器人成功\n" + "3Commas返回:\n "
        #            + json.dumps(response1)) 	tmp_one_deal_Bot_for_binance_new_parie_on_line#2
    else:
        log("update_bot_pairs failed:")
        # send_email("尝试修改DCA机器人："+bot_id+ "交易对为" + coin_pair + "失败\n" + "3Commas返回:\n "
        #            + json.dumps(response1))

if __name__ == '__main__':
    update_pair_of_line_bot("BUSD_BTC", "5455831")