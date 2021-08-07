
import time
import requests
import json
from requests.adapters import HTTPAdapter
from util import log ,send_email,check_and_update_msg
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import daemon
from daemon import pidfile


SCAN_NEW_ARTI_INTERVAL_IN_SEC =60*5
BINANCE_WEB_BASE = 'https://www.binance.com'
_3COMMAS_WEB_URL = 'https://3commas.io/'

# @with_goto
def get_simple_web_data(base_url:str,http_method: str, path: str, payload: any = None, params: str = '',extr_header: any = None):
    requrll = "12"
    if http_method == "GET":
        if params is not None and params != '':
            requrll = base_url + path + '?' + params
        else:
            requrll = base_url + path
    else:#POST/Patch 方法
        requrll = base_url + path
        log("POST 请求方法...")
        if "application/json" in extr_header.values():
            payload = json.dumps(payload).encode('utf8')

    s = requests.Session()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))

    not_get_respon =True

    while not_get_respon :
        not_get_respon = False
        try:
            response = s.request(
                method=http_method,
                url=requrll,
                headers=extr_header,
                data=payload    #传入字典类型 解析 a=b&c=d 放入, content_type =json 需要传入json字符串，不neng传入字典
                , timeout=(3, 2)
                # verify = False
            )
            response.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
        except requests.RequestException as e:
            log("服务器超时重连4次失败:" + requrll + "错误:"+str(e))
            send_email("服务器超时重连3次失败:" + requrll + "错误:"+ str(e))
            log("等待 10s ...重连... ")
            time.sleep(10)
            not_get_respon =True
            continue #重新连接网络


        resp_text= response.text
        if "</x>" in resp_text:
            index_s= resp_text.find("</x>")
            resp_text = resp_text[index_s+4:]
        json_obj = {}
        try:
            json_obj = json.loads(resp_text)
        except (IndexError, IndentationError) as e1:
            log("requrll:" + requrll)
            log("resp:" + response.text)
            log("解析出错" + str(e1))
            send_email("解析出错" + response.text)
            log("等待 5s ...重连... ")
            time.sleep(5)
            not_get_respon =True
            continue #重新连接请求网络

        return json_obj

# @with_goto
def get_simple_web_html(base_url:str,http_method: str, path: str, payload: any = None, params: str = '',extr_header: any = None):
    requrll = "12"
    if http_method == "GET":
        if params is not None and params != '':
            requrll = base_url + path + '?' + params
        else:
            requrll = base_url + path
    else:#POST/Patch 方法
        requrll = base_url + path
        log("POST 请求方法...")
        if "application/json" in extr_header.values():
            payload = json.dumps(payload).encode('utf8')

    s = HTMLSession()
    s.mount('http://', HTTPAdapter(max_retries=3))
    s.mount('https://', HTTPAdapter(max_retries=3))
    # label .begin
    not_get_respon =True
    while not_get_respon :
        not_get_respon = False
        try:
            response = s.request(
                method=http_method,
                url=requrll,
                headers=extr_header,
                data=payload    #传入字典类型 解析 a=b&c=d 放入, content_type =json 需要传入json字符串，不neng传入字典
                , timeout=(3, 2)
                # verify = False
            )
            response.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
        except requests.RequestException as e:
            log("服务器超时重连4次失败:" + requrll + "错误:"+str(e))
            send_email("服务器超时重连3次失败:" + requrll + "错误:"+ str(e))
            log("等待 10s ...重连... ")
            time.sleep(10)
            # goto .begin
            not_get_respon = True
            continue # 调到while 处来进行再一次网络请求

        return response.html


def get_check_anooucement_of_binance():
    print("获取币安交易所通知————————————————————————————————————")
    data_arry = get_simple_web_data(
            base_url=BINANCE_WEB_BASE,
            http_method="GET",
            path="/bapi/composite/v1/public/cms/article/catalog/list/query",
            params="catalogId=48&pageNo=1&pageSize=15",
            extr_header={'lang': 'zh-CN'}
            )

    articles = data_arry['data']['articles']
    # if not check_and_update_msg(str(articles[0]['id']),"binance"):
    #     print("没有新发布文章")
    #     return
    n = 1
    for arti in articles:
        title =arti['title']
        code = arti['code']
        link = BINANCE_WEB_BASE + "/zh-CN/support/announcement/" + code
        log("第"+ str(n) +"条消息:")
        coin_name_arr = parse_bian_title(title,code)
        for coin_name in coin_name_arr:
            check_online_list_on_other_exchange(coin_name,"Binance","币安",link)
        n = n+1

def get_check_anooucement_of_binance_fiat():
    print("法币交易")
    data_arry = get_simple_web_data(
            base_url=BINANCE_WEB_BASE,
            http_method="GET",
            path="/bapi/composite/v1/public/cms/article/list/query",
            params="type=1&catalogId=50&pageNo=1&pageSize=15",
            extr_header={'lang': 'zh-CN'}
            )

    articles = data_arry['data']['catalogs'][0]['articles']
    if not check_and_update_msg(str(articles[0]['id']),"binance_fliat"):
        print("没有新发布文章")
        return
    n = 0
    for arti in articles:
        id = arti['id']
        title =arti['title']
        code = arti['code']
        link =BINANCE_WEB_BASE+"/zh-CN/support/announcement/"+code
        log("第" + str(n) + "条消息:")
        coin_name_arr = parse_bian_title(title,code)
        for coin_name in coin_name_arr:
            check_online_list_on_other_exchange(coin_name,"Binance","币安",link)
        n=n+1


def get_check_anooucement_of_huobi():
    print("获取火币交易所通知————————————————————————————————————")
    data_arry = get_simple_web_data(
            base_url="https://www.huobi.sh",
            http_method="POST",
            path="/support/public/getList",
            extr_header={
                'Content-Type': 'application/json',
                'accept-language': 'zh-cn'
            },
            payload={
                    "language": "zh-cn",
                    "page": 1,
                    "limit": 12,
                    "oneLevelId": 360000031902,
                    "twoLevelId": 360000039942
                    }
            )

    articles = data_arry['data']['list']
    if not check_and_update_msg(str(articles[0]['id']),"huobi"):
        print("没有新发布文章")
        return
    for arti in articles:
        id = arti['id']
        title =arti['title']
        # log("id:"+str(id))
        # log("title:" + title)
        coin_name = parse_huobi_title(title)
        if coin_name!=" ":
            check_online_list_on_other_exchange(coin_name,"Huobi","火币")

def get_check_anooucement_of_kubi():
    print("获取库币交易所通知————————————————————————————————————")
    data_arry = get_simple_web_data(
            base_url="https://www.kucoin.com",
            http_method="GET",
            path="/_api/cms/articles",
            params="page=1&pageSize=2&category=listing&lang=zh_CN"
            )
    articles = data_arry['items']
    if not check_and_update_msg(str(articles[0]['id']),"kubi"):
        print("没有新发布文章")
        return
    for arti in articles:
        # id = arti['id']
        title =arti['title']
        news_publish_time = arti['publish_at']

        # log("id:"+str(id))
        # log("title:" + title)
        log("信息发布时间:" + news_publish_time)
        coin_name = parse_kubi_title(title)
        if coin_name!=" ":
            check_online_list_on_other_exchange(coin_name,"KuCoin","库币")
#https://help.ftx.com/hc/zh-cn/sections/360007186612-%E4%B8%8A%E6%96%B0%E5%85%AC%E5%91%8A
def get_check_anooucement_of_ftx():
    print("获取FTX交易所通知————————————————————————————————————")
    html_obj = get_simple_web_html(
            base_url="https://help.ftx.com/",
            http_method="GET",
            path="/hc/zh-cn/sections/360007186612-%E4%B8%8A%E6%96%B0%E5%85%AC%E5%91%8A",
            )
    arti_list = html_obj.find('li.article-list-item')
    first_arti_title= arti_list[0].text
    print("最新文章"+first_arti_title+"。。。。。。。。。。。")
    if not check_and_update_msg(first_arti_title,"ftx"):
        print("没有新发布文章")
        return
    chek_num=0
    for arti in arti_list:
        title = arti.text
        link=arti.absolute_links
        # news_publish_time = arti['publish_at']

        # log("信息发布时间:" + news_publish_time)
        coin_name = parse_ftx_title(title)
        if coin_name!=" ":
            check_online_list_on_other_exchange(coin_name,"FTX","FTX")
        chek_num = chek_num +1
        if chek_num>1:break

#https://medium.com/_/api/collections/c114225aeaf7/stream?to=1628091783718&page=2
def get_check_anooucement_of_coinbase():
    print("获取coinbase交易所通知————————————————————————————————————")
    json_data = get_simple_web_data(
            base_url="https://medium.com",
            http_method="GET",
            path="/_/api/collections/c114225aeaf7/stream",
            params="to=1628091783718&page=2"
            )

    # print(json_data)
    arti_list = json_data['payload']['references']['Post']
    first_arti_title= str(arti_list.keys())
    print("最新文章"+first_arti_title+"。。。。。。。。。。。")
    if not check_and_update_msg(first_arti_title,"coinbase"):
        print("没有新发布文章")
        return
    chek_num=0
    for (arti_id,arti) in arti_list.items():
        title = arti['title']
        # print(title)
        # print(arti_id)
    #     # link=arti.absolute_links
    # #     # news_publish_time = arti['publish_at']
    # #
    # #     # log("信息发布时间:" + news_publish_time)
        coin_name_arr = parse_coinbase_title(title)
        for coin_name in coin_name_arr:
            check_online_list_on_other_exchange(coin_name,"Coinbase Pro (GDAX)","coinbase")
        # chek_num = chek_num +1
        # if chek_num>3:break


def get_annance_content_of_bian(code):
    html_obj = get_simple_web_html(
            base_url=BINANCE_WEB_BASE,
            http_method="GET",
            path="/zh-CN/support/announcement/"+code,
            )
    arti_content = html_obj.find('div.css-mm1dbi')[0]
    print("消息内容:"+arti_content.text)
    return arti_content.text


def parse_bian_title(title:str="",code:str=""):
    print("消息标题："+title)
    coin_name_arr = []
    if "币安上市" in title or "币安创新区上市" in title:
        index_s = title.find('（')
        index_e = title.find("）")
        coin_name_s =title[index_s+1:index_e]
        print("提取货币简写"+coin_name_s)
        coin_name_arr.append(coin_name_s)
        return coin_name_arr

    elif "币安新增" in title and "交易对" in title\
       or"币安上线" in title and "交易对" in title:
        content=get_annance_content_of_bian(code)
        if "币安将于" in content and "上线" in content:
            index_s = content.find('币安将于')
            index_e = content.find("上线")
            index_ee = content.find("交易对")
            on_line_date = content[index_s+4:index_e].strip()
            pairs_str = content[index_e+2:index_ee].strip()
            # print("on_line_date: " + on_line_date)
            # print("pairs_str: "+pairs_str)
            if "USDT" in pairs_str or "BUSD" in pairs_str:
                pair_grp= pairs_str.split('、')
                for pair in pair_grp:
                    if pair.find('USDT')>0:
                        index = pair.find('USDT')
                        coin_name_s = pair[0:index-1]
                        coin_name_arr.append(coin_name_s)
                    elif pair.find('BUSD') > 0:
                        index = pair.find('BUSD')
                        coin_name_s = pair[0:index-1]
                        coin_name_arr.append(coin_name_s)

        if len(coin_name_arr)!=0:
            print("提取货币简写" + str(coin_name_arr)+"\n")
        else:
            print("没有可交易货币...\n")
        return coin_name_arr

    else:
        print("非上新通知...\n")
        return coin_name_arr

def parse_huobi_title(title:str=""):
    if "上线新币" in title:
        index_s = title.find("上线新币")
        index_e = title.find('（')
        if index_e ==-1 :
            return " "
        coin_name_s =title[index_s+len("上线新币"):index_e]
        print("货币简写"+coin_name_s)
        return coin_name_s
    else:
        return " "

def parse_kubi_title(title:str=""):
    if "KuCoin上线" in title:
        index_s = title.find('(')
        index_e = title.find(")")
        if index_s == -1 or index_e == -1:
            return " "
        coin_name_s =title[index_s+1:index_e]
        print("货币简写"+coin_name_s)
        return coin_name_s
    else:
        return " "

def parse_ftx_title(title:str=""):
    if "FTX现已上线" in title:
        index_s = title.find('(')
        index_e = title.find(")")
        if index_s == -1 or index_e == -1:
            return " "
        coin_name_s =title[index_s+1:index_e]
        type = title[index_e+1:]
        print("货币简写"+coin_name_s + "["+type+"]")
        return coin_name_s
    else:
        return " "

def parse_coinbase_title(title:str=""):
    if "launching on Coinbase" in title:
        coin_name_arr =[]
        index_e =0
        while index_e!=-1:
            index_s = title.find('(',index_e+1)
            index_e = title.find(")",index_e+1)
            if index_s ==-1 or index_e==-1:
                break
            coin_name_s =title[index_s+1:index_e]
            coin_name_arr.append(coin_name_s)


        print("货币简写(多个)"+str(coin_name_arr))
        return coin_name_arr
    else:
        return []

def check_online_list_on_other_exchange(coin_name,prepare_exc,prepare_exc_Chinese,link:str=""):
    # print("检查其他交易所上线情况")
    #deal excpetion
    if coin_name=="SHIB":
        return
    data_arry = get_simple_web_data(
            base_url=_3COMMAS_WEB_URL,
            http_method="GET",
            path="exchanges.json",
            params="codes[]=binance&"
               "codes[]=ftx&"
               "codes[]=kucoin&"
               "codes[]=gate_io&"
               "codes[]=huobi&"
               "codes[]=okex&"
               "codes[]=gdax&" #coinbase 标识代码gdax
               "pairs=true"
            )
    print("检查结果：")
    print("---------------"+coin_name+"-------------------------------")
    on_listed_exch =[]
    for exchange in data_arry['exchanges']:
        ex_name = exchange["name"]
        pairs = exchange['data']['pairs']
        if  "USDT_"+coin_name in pairs or\
            "BUSD_"+coin_name in pairs or \
            "USD_" + coin_name in pairs or \
            "USDC_" + coin_name in pairs or \
            "HUSD_" + coin_name in pairs:   ####okex
            print("【"+prepare_exc+"】"+coin_name+"已经在交易所："+ex_name+"上线")
            on_listed_exch.append(ex_name)
    print("-----------------"+coin_name+"-------check_end--------------")

    if  prepare_exc in on_listed_exch:
        print("已经在本交易所上线，不发送通知\n")
        return 
        
    print(coin_name +"近期将上线["+prepare_exc_Chinese+"]交易所，目前已经上线该币的交易所有:"
         +str(on_listed_exch)+"\n通知链接 "+link,
      "交易所上新通知")
    log("发送通知邮件..")
    send_email(coin_name + "近期将上线[" + prepare_exc_Chinese + "]交易所，目前已经上线该币的交易所有:"
               + str(on_listed_exch)+"\n通知链接 "+link,
              "交易所上新通知")


#前台进程版本  （日志打印在控制台）
def do_main_thing():
    # while(True):
        get_check_anooucement_of_binance()
        get_check_anooucement_of_binance_fiat()
        # get_check_anooucement_of_huobi()
        # get_check_anooucement_of_kubi()
        # get_check_anooucement_of_ftx()
        # # get_check_anooucement_of_okcoin()
        # # get_check_anooucement_of_gate_io()
        # # get_check_anooucement_of_bittrex()
        # get_check_anooucement_of_coinbase()
        # time.sleep(SCAN_NEW_ARTI_INTERVAL_IN_SEC)

def do_main_thing_indaemon():
# 2.后台进程版本 ，linux服务器上，跑所需要的
#参考https://www.codenong.com/13106221/

# pid_f = "/root/daemon_on_line_updater.pid"
    logfile = open('/root/daemon.log', 'w')
    with daemon.DaemonContext(stdout=logfile,stderr=logfile) as context:
        while(True):
            get_check_anooucement_of_binance()
            get_check_anooucement_of_binance_fiat()
            get_check_anooucement_of_huobi()
            get_check_anooucement_of_kubi()
            get_check_anooucement_of_ftx()
            get_check_anooucement_of_coinbase()
            time.sleep(SCAN_NEW_ARTI_INTERVAL_IN_SEC)


#前台进程版本  （日志打印在控制台）
if __name__ == '__main__':
    do_main_thing()
    # do_main_thing_indaemon()



