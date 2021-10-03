import datetime
import time

from py3commas.request import Py3Commas
from util import log, send_email, read_news_title_with_speaker, log_to_file
from config import *

balance_status = "left_money_ok"
ORDER_CHECK_INTERVAL_IN_MINS =1 # 加仓间隔，最小加仓间隔 1min/3min 效果较好
#6615账户的 key 和 secr  bot_id----4228101
# p3c_ = Py3Commas(key='08e94c4768d44f3a9a6f14f68f86a2a63d3dfe67f18c4f28905afad93dfadb92',
#                 secret='742ce7cffb40f42883e0c454652ebad5d3ccfb125b283b92214401547ea73a'
#                        'b2647f42a44e68544054ab9a70769dcfb890fdffe4a181a984287dc8d3e783'
#                        'db9a7c501aaacec88af608f0e135f5c2323f921181ea2023176068396eb973'
#                        '2c18c487240ec0')
#1324907549@qq.com 账户key  bot_id-==---5601757
p3c = Py3Commas(key='xx',
                secret='xx'
                       ' '
                       ' '
                       ' ')

def do_deal_check_and_order():
    check_all_deals_to_funds()
    pass



def update_max_safety_orders():
    # POST /ver1/deals/{deal_id}/update_max_safety_orders
    pass

# 计算添加的coin的数量
def cacalate_quatity_so_single(so_num:int=8,safety_order:float=100.0,current_price:float=1.0):
    print("safety_order1="+str(safety_order))
    usd_quantity_tot =0
    for i in range(so_num,so_num+1) :
        order_n  =  safety_order*pow(1.18,i-1)
        print("order_n"+str(i)+"=="+str(order_n)[0:6])
        usd_quantity_tot = usd_quantity_tot + order_n
    print("usd_@so"+str(so_num)+"="+str(usd_quantity_tot)[0:6]+"busd")
    coin_quantity_tot= usd_quantity_tot/current_price
    print("coin__@_so" + str(so_num) + "=" + str(coin_quantity_tot)[0:6] + "coin")
    return coin_quantity_tot

# 计算添加的coin的数量
def cacalate_quatity_so_sum(so_num:int=8,safety_order:float=100.0,current_price:float=1.0):
    print("safety_order1="+str(safety_order))
    usd_quantity_tot =0
    for i in range(2,so_num+1) :
        order_n  =  safety_order*pow(1.18,i-1)
        print("order_n"+str(i)+"=="+str(order_n)[0:6])
        usd_quantity_tot = usd_quantity_tot + order_n
    print("usd_total_add_at_so[2-"+str(so_num)+"]="+str(usd_quantity_tot)[0:6]+"busd")
    coin_quantity_tot= usd_quantity_tot/current_price
    print("coin_quantity_tot_at_so[2-" + str(so_num) + "]=" + str(coin_quantity_tot)[0:6] + "coin")
    return coin_quantity_tot

#[添加一个限价单]
def add_funds_at_limit_pri_with_so_single(deal_id:str="123",so_num:int=3,safety_order:float=100.0,current_price:float=1.0):

    coin_quantity = cacalate_quatity_so_single(so_num,safety_order,current_price)
    print(coin_quantity)
    # POST /ver1/deals/{deal_id}/add_funds
    response1 = p3c.request(
        entity='deals',
        action='add_funds',
        _id=deal_id,                   
        payload={"deal_id": deal_id,     
                 "quantity": coin_quantity,  # 添加的 base_coin 数量
                 "is_market": "false", #
                 "rate": current_price*0.99, #添加的 限价单 的价格 (限价单时使用)
                 }
    )
    usd_quantity =coin_quantity*current_price
    print("response1:"+str(response1))
    if "error" in response1:
        print("交易id"+str(deal_id)+" 添加限价单出错 "+str(usd_quantity)+" USD ")#
        if 'not_enough_money'==response1['error']:
            print("错误原因,资金不足: "+response1['error_description'])
            return 1 #资金不足
        else:
            print("错误原因: " + response1['error_description'])
            return -1 #其他原因
    else:
        log_to_file("交易id"+str(deal_id)+" 添加限价单成功，数量:"+str(usd_quantity)+" USD at price "+str(current_price*0.99),"auto_add_balance.log")#
        return 0

#[一次性加仓]
def add_funds_at_market_pri_with_so_sum(deal_id:str="123",so_num:int=3,safety_order:float=100.0,current_price:float=1.0):

    coin_quantity = cacalate_quatity_so_sum(so_num,safety_order,current_price)
    print(coin_quantity)
    # POST /ver1/deals/{deal_id}/add_funds 
    response1 = p3c.request(
        entity='deals',
        action='add_funds',
        _id=deal_id,     # deal_id
        payload={"deal_id": deal_id, # 虚拟账户
                 "quantity": coin_quantity,  # 添加的 base_coin 数量
                 "is_market": "true", #
                 # "rate": "17", #添加的 限价单 的价格 (限价单时使用)
                 }
    )
    usd_quantity =coin_quantity*current_price
    print("response1:"+str(response1))
    if "error" in response1:
        print("交易id"+str(deal_id)+" 添加资金出错 "+str(usd_quantity)+" USD ")#
        if 'not_enough_money'==response1['error']:
            print("错误原因,资金不足: "+response1['error_description'])
            return 1 #资金不足
        else:
            print("错误原因: " + response1['error_description'])
            return -1 #其他原因
    else:
        log_to_file("交易id"+str(deal_id)+" 添加资金成功，市价单，数量:"+str(usd_quantity)+" USD","auto_add_balance.log")#
        return 0

#检查可用的busd
def check_left_money():
    print("尝试获取账户资金余额...")
    # //POST// /ver1/accounts/{account_id}/account_table_data
    response1 = p3c.request(
        entity='accounts',
        action='account_table_data',
        _id="30863718",
        payload={"account_id": "30863718"}
    )
    usd_left = 0
    for item in response1:
        if item['currency_code']=="BUSD":
            usd_left=item['position']

    one_add_usd_amount=cacalate_quatity_so_sum(FIRST_MAN_ADD_FUND_SO, 75.00, 1)
    print("添加最小需要的usd: "+str(one_add_usd_amount)+"USD")
    print("剩余可用USD余额  : " + str(usd_left) + " USD")
    if usd_left<one_add_usd_amount:
        return "left_money_insufficient"
    else:
        return "left_money_enough"


def check_all_deals_to_funds():
    print("尝试获取正在运行的订单...")
    response1 = p3c.request(
        entity='deals',
        action='',
        # param="bot_id=4228101&scope=active", #4228101
        param="bot_id=5601757&scope=active",  # 5601757 --132 safari 账户
    )
    active_deal_cnt = len(response1)
    print("活跃的订单数目 ["+str(active_deal_cnt)+"]")

    for deal_data in response1:
        print(deal_data)
        to_currency = deal_data['to_currency']
        finished = deal_data['finished?']
        completed_so_count = deal_data['completed_safety_orders_count']
        completed_man_order_count = deal_data['completed_manual_safety_orders_count']
        deal_id = str(deal_data['id'])
        created_at = deal_data['created_at']
        updated_at = deal_data['updated_at']
        safety_order = deal_data['safety_order_volume']
        current_price = deal_data['current_price']
        cur_profit_per = deal_data['actual_profit_percentage']
        pair_name = to_currency+"/BUSD"
        print("deal_id:"+str(deal_id))
        created_day = str((created_at)[8:10])
        created_hour = str((created_at)[11:13])
        cur_day =  str(datetime.datetime.now().strftime("%d"))
        cur_hour = str(datetime.datetime.now().strftime("%H"))
        duration_day= int(cur_day) - int(created_day)
        duration_hours = duration_day*24 + int(cur_hour) - int(created_hour)

        # # print("持续时间："+str(int(duration_hours/24))+"days"+str(duration_hours%24)+"hours")
        # if duration_hours >24*3  : #订单超过3天
        #     print("订单持续时间:"+str(duration_hours)+"小时，超过24*3小时，理会???")
        #     # read_news_title_with_speaker(pair_name+"订单持续时间:"+str(duration_hours)+"小时，超过24*3小时")
        #     # continue

        # print("订单持续时间："+str(duration_hours)+"hours < 24*3小时 ")
        add_fund_so=FIRST_MAN_ADD_FUND_SO
        add_fund_fall_percent=-add_fund_so*2
        if completed_man_order_count ==0: #1.尚未添加man订单
             if  float(cur_profit_per)<add_fund_fall_percent and \
                 completed_so_count <3: #3.自动订单数so_compelit<3
                log(pair_name + "当前回撤为" + str(cur_profit_per) + "%, 大于"+str(add_fund_fall_percent)+"%+程序添加SO-2到"+str(add_fund_so)+"级别的资金")

                ret = add_funds_at_market_pri_with_so_sum(deal_id,add_fund_so,float(safety_order),float(current_price))
                if ret==0:
                    log_to_file(pair_name+"添加SO-"+str(add_fund_so)+"级别的资金成功","auto_add_balance.log")
                    read_news_title_with_speaker(str((pair_name))+"添加SO-"+str(add_fund_so)+"级别的资金")
                elif ret==1:
                    log_to_file(pair_name+"添加资金失败,资金不足,程序退出","auto_add_balance.log")
                    # read_news_title_with_speaker(pair_name + "添加资金失败，资金不足，程序退出")
                    exit(0) #程序直接终止，等待下一次crontab拉起
                else:
                    log_to_file(pair_name + "添加资金失败,其他原因", "auto_add_balance.log")
                    #    # 其他原因(网络原因)，再次循环，尝试
        elif completed_man_order_count >0:
            if float(cur_profit_per) < 2.5 \
                and completed_so_count < 3:  # 3.自动DCA单so_compelit<3
                print("添加初始" + str(FIRST_MAN_ADD_FUND_SO) + "单基础上")
                log(pair_name + "当前回撤为" + str(cur_profit_per) + "%, 大于" + "2.5%+程序添加SO-" + str(FIRST_MAN_ADD_FUND_SO+completed_man_order_count+1-1) + "单的资金")
        
                ret = add_funds_at_limit_pri_with_so_single(deal_id, add_fund_so, float(safety_order), float(current_price))
                if ret == 0:
                    log_to_file(pair_name + "添加SO-" + str(add_fund_so) + "单的资金成功", "auto_add_balance.log")
                    read_news_title_with_speaker(str((pair_name)) + "添加SO-" + str(add_fund_so) + "单的资金")
                elif ret == 1:
                    log_to_file(pair_name + "添加资金失败,资金不足,程序退出", "auto_add_balance.log")
                    # read_news_title_with_speaker(pair_name + "添加资金失败，资金不足，程序退出")
                    exit(0)  # 程序直接终止，等待下一次crontab拉起
                else:
                    log_to_file(pair_name + "添加资金失败,其他原因", "auto_add_balance.log")

        else:
            log(pair_name+"当前回撤为"+str(cur_profit_per)+"%, 小于"+str(add_fund_fall_percent)+"%，不用程序添加资金")


#-定时检查 回调百分比12%，加仓 6 单，后面的正常加单[一定程度上，避免前7 单前的解套失败， 分批解套，519、720情形有一点改善、阴跌恶性币，效果一般]
if __name__ == '__main__':  #一般就开2-3个机器人，风险考虑

    balance_status = check_left_money()
    if 'left_money_insufficient' == balance_status :
        log("账户资金不足...程序退出... ")
        # read_news_title_with_speaker("警告：账户资金不足...,风险考虑，请减小并发订单，或者添加资金")
        exit(0)

    while (True):
        do_deal_check_and_order()
        log("等待"+str(ORDER_CHECK_INTERVAL_IN_MINS)+"min 再次订单检查") #1min/3min 预防急跌效果较好
        time.sleep(ORDER_CHECK_INTERVAL_IN_MINS*60) 

