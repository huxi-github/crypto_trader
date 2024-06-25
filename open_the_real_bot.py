import datetime
import time
from playsound import playsound
from py3commas.request import Py3Commas
from util import log, send_email, read_news_title_with_speaker, log_to_file
from config_5UP_filter import real_bot_id,emmu_bot_id,real_account_id,emu_account_id,market_over_crazy_threshold
from muti_dca_deal_creator import start_new_deal,p3c


# def do_deal_check_and_order():
#     check_all_deals_to_funds()
#     pass

def start_the_bot(bot_id:str="11358971"):
    response1 = p3c.request(
        entity='bots',
        action='enable',
        _id=bot_id,                   
        payload={"bot_id": bot_id
                 }
    )
    # print(response1)
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
        _id=real_account_id,
        payload={"account_id": real_account_id}
    )

    # print(response1)
    usd_left = 0
    day_profit_usd =0
    for item in response1:
        if item['currency_code']=="USDT":
            usd_left=item['position']

    # one_add_usd_amount=cacalate_quatity_so_sum(FIRST_MAN_ADD_FUND_SO, 75.00, 1)
    one_add_usd_amount=400*7
    print("剩余可用USD余额  : " + str(usd_left) + " USD")
    if usd_left<one_add_usd_amount:
        return "left_money_insufficient"
    else:
        return "left_money_enough"


if __name__ == '__main__':  #一般就开2-3个机器人，风险考虑
    PROXY_ERRO_INTERVAL_IN_SEC =60 #s
    log_to_file_path = "open_the_real_bot.log"
    bot_id = real_bot_id
    while (True):
        try:
            return_str = check_left_money()
            log_to_file("当前账户金额 "+return_str,log_to_file_path)
            currentDateAndTime = datetime.datetime.now()

            if "left_money_insufficient" in return_str:
                print("账户资金余额不足")
                log_to_file("账户资金余额不足 ",  log_to_file_path)
                playsound("audio/alert.mp3")
                read_news_title_with_speaker("账户资金余额不足")
                # stop_the_bot(bot_id)#模拟 
                send_email("open_the_real_bot 账户资金余额不足","账户资金余额不足")   

            if "left_money_enough" in return_str:
                print("账户资金余额OK")
                log_to_file("账户资金余额OK ",  log_to_file_path)  
                start_the_bot(bot_id)  
                break

        except Exception as e:
            log_to_file(f"发生异常: {e}",log_to_file_path)
            log_to_file("发生异常,网络问题崩溃,等待 " + str(PROXY_ERRO_INTERVAL_IN_SEC / 60) + "min 再次查找",log_to_file_path)
            time.sleep(PROXY_ERRO_INTERVAL_IN_SEC)
            continue

