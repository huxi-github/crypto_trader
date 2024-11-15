import datetime
import time
from playsound import playsound
from py3commas.request import Py3Commas
from util import log, send_email, read_news_title_with_speaker, log_to_file
from config_5UP_filter import real_bot_id,emmu_bot_id,real_account_id,emu_account_id,market_over_crazy_threshold
from muti_dca_deal_creator import start_new_deal,p3c

balance_status = "left_money_ok"
ORDER_CHECK_INTERVAL_IN_MINS =15 # 加仓间隔，最小加仓间隔 1min/3min 效果较好

bot_id=real_bot_id
threshold=market_over_crazy_threshold

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
    # print(response1)

def close_deal_with_market_price(deal_id:str=""):
    # ('POST', '{id}/panic_sell_all_deals'),
    print("强制市场价关闭所有订单===================================")
    response1 = p3c.request(
        entity='bots',
        action='panic_sell_all_deals',
        _id=bot_id,
        payload={"bot_id": bot_id}
    )
    # print(response1)


def get_today_profit(account_id:str,bot_id:str):
    # print("尝试获取正在运行的订单...")
    response1 = p3c.request(
        entity='bots',
        action='stats',
        param="bot_id="+bot_id+"&account_id="+account_id
    )

    # print(response1)
    day_profit_usd =0
    day_profit_usd= response1['profits_in_usd']['today_usd_profit']
    # print("当日利润："+day_profit_usd) 
    return day_profit_usd

def check_all_deals_to_profit_and_close(bot_id:str):
    # print("尝试获取正在运行的订单...")
    # response1 = p3c.request(
    #     entity='deals',
    #     action='',
    #     # param="bot_id=4228101&scope=active", #4228101
    #     param="bot_id="+bot_id+"&scope=active",  # 5601757 --132 safari 账户
    # )
    # # print(response1)
    # active_deal_cnt = len(response1)
    # print("活跃的订单数目 ["+str(active_deal_cnt)+"]")

    # update_deal_tp(deal_id,"1")
    close_deal_with_market_price(bot_id)
    today_PL=get_today_profit("",bot_id)
    log_to_file("卖掉所有订单后的今日盈亏是"+str(today_PL),log_to_file_path)
    send_email("单日利润金额大于阈值 "+str(threshold)+"(市场空前繁荣告警)暂停机器人4天,并关闭所有订单...,产生的损益:" + str(today_PL)+"usd","市场空前繁荣告警")



if __name__ == '__main__':  #一般就开2-3个机器人，风险考虑
    PROXY_ERRO_INTERVAL_IN_SEC =60 #s
    Frame_level= '15m'
    log_to_file_path = "auto_balance_checker_"+Frame_level+".log"
    # check_all_deals_to_profit_and_close()
    # send_email("单日利润金额大于阈值 "+str(threshold)+"(市场空前繁荣告警)暂停机器人4天,并关闭所有订单" + str(10000)+"usd","市场空前繁荣告警")

    while (True):
        try:
            today_profit = get_today_profit("",bot_id)
            log_to_file("当前利润金额 "+str(today_profit),log_to_file_path)
            currentDateAndTime = datetime.datetime.now()
            if currentDateAndTime.hour ==7 and currentDateAndTime.minute>40:
                log_to_file("单日利润金额=======>"+str(today_profit),log_to_file_path)
            if today_profit>threshold:
                print("单日利润金额大于阈值 "+str(threshold)+"暂停机器人4天,并关闭部分订单...")
                log_to_file("单日利润金额大于阈值 "+str(threshold)+"(市场空前繁荣告警)暂停机器人4天,并关闭部分订单...",log_to_file_path)
                playsound("audio/alert.mp3")
                read_news_title_with_speaker("市场空前繁荣告警")
                stop_the_bot(bot_id)#模拟 
                # stop_the_bot(real_bot_id)
                check_all_deals_to_profit_and_close(bot_id)    
                # check_all_deals_to_profit_and_close(real_bot_id)   
                send_email("单日利润金额大于阈值 "+str(threshold)+"(市场空前繁荣告警)暂停机器人4天,并关闭所有订单" + str(today_profit)+"usd","市场空前繁荣告警")          
            print("等待"+str(ORDER_CHECK_INTERVAL_IN_MINS)+"min ")  
            time.sleep(ORDER_CHECK_INTERVAL_IN_MINS*60) 
        except Exception as e:
            log_to_file(f"发生异常: {e}",log_to_file_path)
            log_to_file("发生异常,网络问题崩溃,等待 " + str(PROXY_ERRO_INTERVAL_IN_SEC / 60) + "min 再次查找",log_to_file_path)
            time.sleep(PROXY_ERRO_INTERVAL_IN_SEC)
            continue

