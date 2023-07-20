import datetime
import time

from py3commas.request import Py3Commas
from util import log, send_email, read_news_title_with_speaker, log_to_file
from config import *
from muti_dca_deal_creator import start_new_deal,p3c

balance_status = "left_money_ok"
ORDER_CHECK_INTERVAL_IN_MINS =15 # 加仓间隔，最小加仓间隔 1min/3min 效果较好
real_bot_id ="11367606"
emmu_bot_id ="11358971"

account_id="30391014"

def do_deal_check_and_order():
    check_all_deals_to_funds()
    pass

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
    if disabled:
        print("成功关闭机器人:"+bot_id)
        return True
    else:
        print("未能关闭机器人:"+bot_id)
        return False


#检查可用的busd
def check_left_money():
    print("尝试获取账户资金余额...")
    # //POST// /ver1/accounts/{account_id}/account_table_data
    response1 = p3c.request(
        entity='accounts',
        action='account_table_data',
        _id="30391014",
        payload={"account_id": "30391014"}
    )

    print(response1)
    usd_left = 0
    day_profit_usd =0
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

def update_deal_tp(deal_id:str="",tp:str="1"):
    # POST /ver1/deals/{deal_id}/update_tp
    response1 = p3c.request(
        entity='deals',
        action='update_tp',
        _id=deal_id,
        payload={"deal_id": deal_id,
        "new_take_profit_percentage":tp}
    )
    print(response1)


def get_today_profit(account_id:str,bot_id:str):
    print("尝试获取正在运行的订单...")
    response1 = p3c.request(
        entity='bots',
        action='stats',
        payload={"account_id": account_id,
        "bot_id":bot_id}
    )

    print(response1)
    day_profit_usd =0
    day_profit_usd= response1['profits_in_usd']['today_usd_profit']
    # print("当日利润："+day_profit_usd) 
    print("当日利润："+str(day_profit_usd))
    return day_profit_usd

def check_all_deals_to_profit_and_close(bot_id:str):
    print("尝试获取正在运行的订单...")
    response1 = p3c.request(
        entity='deals',
        action='',
        # param="bot_id=4228101&scope=active", #4228101
        param="bot_id="+bot_id+"&scope=active",  # 5601757 --132 safari 账户
    )
    print(response1)
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

        update_deal_tp(deal_id,"1")

        # # print("持续时间："+str(int(duration_hours/24))+"days"+str(duration_hours%24)+"hours")
        # if duration_hours >24*3  : #订单超过3天
        #     print("订单持续时间:"+str(duration_hours)+"小时，超过24*3小时，理会???")
        #     # read_news_title_with_speaker(pair_name+"订单持续时间:"+str(duration_hours)+"小时，超过24*3小时")
        #     # continue

        # print("订单持续时间："+str(duration_hours)+"hours < 24*3小时 ")
        '''
        manual_profit_percent=1

        if completed_man_order_count ==0: #1.尚未添加man订单
             if  float(cur_profit_per)>manual_profit_percent and \
                 completed_so_count <3: #3.自动订单数so_compelit<3
                log(pair_name + "当前回撤为" + str(cur_profit_per) + "%, 大于紧急情况强制手动结束单 获利"+str(manual_profit_percent)+"% 订单提前止盈")

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
                    #    # 其他原因(网络原因)，再次循环，尝

        else:
            log(pair_name+"当前回撤为"+str(cur_profit_per)+"%, 小于"+str(add_fund_fall_percent)+"%，不用程序添加资金")
        '''

if __name__ == '__main__':  #一般就开2-3个机器人，风险考虑
    PROXY_ERRO_INTERVAL_IN_SEC =60 #s
    Frame_level= '15m'
    log_to_file_path = "auto_balance_checker_"+Frame_level+".log"
    # check_all_deals_to_profit_and_close()
    while (True):
        try:
            today_profit = get_today_profit(account_id,real_bot_id)
            if today_profit>110:
                print("单日利润金额大于阈值 "+str(110)+"暂停机器人4天,并关闭部分订单...")
                log_to_file("单日利润金额大于阈值 "+str(110)+"暂停机器人4天,并关闭部分订单...",log_to_file_path)
                stop_the_bot("11367606")
                stop_the_bot("11358971")#模拟   
                check_all_deals_to_profit_and_close(real_bot_id)             
                send_email("单日利润金额大于阈值 "+str(110)+"暂停机器人4天,并关闭部分订单...:" + str(today_profit)+"usd",log_to_file_path)
            print("等待"+str(ORDER_CHECK_INTERVAL_IN_MINS)+"min 再次订单")  
            time.sleep(ORDER_CHECK_INTERVAL_IN_MINS*60) 
        except Exception as e:
            print(f"发生异常: {e}")
            log("发生异常,网络问题崩溃,等待 " + str(PROXY_ERRO_INTERVAL_IN_SEC / 60) + "min 再次查找")
            time.sleep(PROXY_ERRO_INTERVAL_IN_SEC)
            continue

