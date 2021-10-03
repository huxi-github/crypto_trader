import hashlib
import hmac
import requests
import json
from urllib import parse
from requests.adapters import HTTPAdapter
import urllib3
import time

from goto import with_goto

from .config import API_URL, API_VERSION, APIS, BINANCE_API_BASE,BINANCE_WEB_BASE
from util import send_email,log

class Py3Commas:

    def __init__(self, key: str, secret: str):
        if key is None or key == '':
            raise ValueError('Missing key')
        if secret is None or secret == '':
            raise ValueError('Missing secret')

        self.key = key
        self.secret = secret

    def _generate_signature(self, path: str, data: str) -> str:
        byte_key = str.encode(self.secret)
        message = str.encode(API_VERSION + path + data)
        signature = hmac.new(byte_key, message, hashlib.sha256).hexdigest()
        return signature

    @with_goto# for 3comas  为 开启订单准备的
    def _make_request(self, http_method: str, path: str, params: any, payload: any):
        requrll = ''
        if http_method=="GET":
            signature = self._generate_signature(path, params)
            requrll = API_URL + API_VERSION + path + '?' + params
        else:
            querstr=''
            for key in payload.keys():
                if querstr=='':
                    querstr = querstr+str(key)+'='+str(payload[key])
                else:
                    querstr = querstr +'&'+ str(key) + '=' + str(payload[key])
            log("querstr:" + querstr)
            signature = self._generate_signature(path, querstr)
            # print("APIKEY:" + self.key)
            # print("Signature:" + signature)
            requrll = API_URL + API_VERSION + path+'?'+querstr
        print("requrll==【"+http_method+"】"+requrll)
        label .begin
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=5))
        s.mount('https://', HTTPAdapter(max_retries=5))
        try:
            response = s.request(
                method=http_method,
                url=requrll,
                headers={
                    'APIKEY': self.key,
                    'Signature': signature,
                    'Content-Type':'application/x-www-form-urlencoded'
                }#,data=payload  # python 字典 解析 对应Content-Type +全部放在 url_param 里面
                ,timeout=6
            )
            response_text = response.text
            response.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常 （过于武断）
        except requests.RequestException as e:
            if "422 Client Error" in str(e):
                print("3commas服务器返回str：" + response_text)
                if "Maximum active deals reached" in response_text:
                    print("大于最大 交易数量。。，跳过次交易,暂停一段时间再【筛选判定交易对】，请求3commas机器人")#需要15s 之后再判断--
                    response_text='{"rejected-max-deal":"422","desc":"大于最大交易数"}'
                if "The pair is not in bot pairs list" in response_text:
                    print("交易对"+"不存在备选列表，或者位于黑名单中，直接跳过次交易")  # 需要15s 之后再判断--
                    response_text = '{"rejected-not-exsit":"422-1","desc":"交易对不存在"}'
            if "HTTPSConnectionPool" in str(e):
                log("连接3commas服务器(出错)原因超时："+ str(e))
                print("等待3commas 交易,..重连了重连4次...放弃...是开启订单..秒级操作，条件可能有变.. .. 检查再决定是否开启,发封邮件记录事件")
                send_email("3commas服务器超时重连4次(2,3)，网络问题出错:"+requrll+"\n异常错误:"+str(e)) #[上一层发邮件]
                response_text = '{"net_timeout":"345","desc":"网络拥塞"}'

        json_obj ={}
        try:
            # print("解析resp_json="+response_text)
            json_obj = json.loads(response_text)
        except (IndexError, IndentationError) as e1:
            log("requrll:" + requrll)
            log("resp:" + response_text)
            log("解析出错" + str(e1))
            send_email("解析出错"+response.text)
            log("等待 3s ...重连... ")
            time.sleep(3)
            goto .begin
        return json_obj

    def request(self, entity: str, action: str = '', _id: str = None, payload: any = None,param: str = ''):
        if entity is None or entity == '':
            raise ValueError('Missing entity')
        if entity not in APIS:
            raise ValueError('Invalid entity')
        if action not in APIS[entity]:
            raise ValueError('Invalid action')

        api = APIS[entity][action]
        api_path = api[1]
        if '{id}' in api_path:
            if _id is None or _id == '':
                raise ValueError('Missing id')
            api_path = api_path.replace('{id}', _id)

        if api_path is None or api_path== '':
            return self._make_request(
                http_method=api[0],
                path=entity,
                params=param,
                payload=payload
            )
        else:
            return self._make_request(
                http_method=api[0],
                path=entity + "/" + api_path,
                params=param,
                payload=payload
            )

    # @with_goto
    def request_binance_data(self, http_method: str, path: str, payload: any = None,params: str = ''):
        requrll = ''
        if http_method=="GET":
            signature = self._generate_signature(path, params)
            if params is not None and params !='':
                requrll =BINANCE_API_BASE + path + '?' + params
            else:
                requrll = BINANCE_API_BASE + path
        else:
            querstr=''
            for key in payload.keys():
                if querstr=='':
                    querstr = querstr+str(key)+'='+str(payload[key])
                else:
                    querstr = querstr +'&'+ str(key) + '=' + str(payload[key])
            signature = self._generate_signature(path, querstr)
            log("querstr:" + querstr)
            requrll = BINANCE_API_BASE + path

        # label .begin
        get_response =False
        sleep_retry_times_left =2
        sleep_parse_retry_times_left = 2
        response = None
        json_obj = {}
        while not get_response and sleep_retry_times_left>0 and sleep_parse_retry_times_left>0:
            print("2222requrll="+requrll)
            s = requests.Session()
            s.mount('http://', HTTPAdapter(max_retries=3))
            s.mount('https://', HTTPAdapter(max_retries=3))
            try:
                response = s.request(
                    method=http_method,
                    url=requrll,
                    headers={
                        'APIKEY': self.key,
                        'Signature': signature,
                        'Content-Type':'application/x-www-form-urlencoded'
                    }
                    # ,data=payload  # python 字典 解析 对应Content-Type +全部放在 url_param 里面
                    ,timeout=(3,2)
                )
                response.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
            except requests.RequestException as e:
                if "HTTPSConnectionPool" in str(e) and\
                    "Max retries exceeded" in str(e) :
                    log("币安服务器超时重连3次失败:" + requrll +"\n错误:"+ str(e))
                    log("等待 5s ...重连... ")
                    send_email("币安服务器超时(VPN时延过大)重连3次失败:"+requrll+"错误:"+str(e)+"等待 5s ...重连")
                    time.sleep(5)
                    # goto .begin
                    sleep_retry_times_left = sleep_retry_times_left-1
                    continue
                else:
                    log("币安服务器超时重连3次失败____:" + requrll + "\n错误:" + str(e))
                    log("等待 5s ...重连... ")
                    send_email("币安服务器超时(VPN时延过大)重连3次失败_____xxx:" + requrll + "错误:" + str(e)+"等待 5s ...重连")
                    time.sleep(5)
                    # goto.begin
                    continue
            log("requrll:" + requrll)

            try:
                json_obj = json.loads(response.text)
            except (IndexError, IndentationError) as e1:
                log("requrll:" + requrll)
                log("resp:" + response.text)
                log("解析出错" + str(e1))
                send_email("resp_json解析出错 "+response.text)
                log("等待 2s ...重新请求... ")
                time.sleep(2)
                # goto .begin
                sleep_parse_retry_times_left = sleep_parse_retry_times_left - 1
                continue
            get_response=True
        if not get_response or json_obj == {}:
            json_obj ={'net_erro':'多次尝试网络出错'}
        return json_obj

    @with_goto
    def get_binance_web_data(self, http_method: str, path: str, payload: any = None,params: str = ''):
        requrll = ''
        if http_method=="GET":
            signature = self._generate_signature(path, params)
            if params is not None and params !='':
                requrll =BINANCE_WEB_BASE + path + '?' + params
            else:
                requrll = BINANCE_WEB_BASE + path
        else:
            querstr=''
            for key in payload.keys():
                if querstr=='':
                    querstr = querstr+str(key)+'='+str(payload[key])
                else:
                    querstr = querstr +'&'+ str(key) + '=' + str(payload[key])
            signature = self._generate_signature(path, querstr)
            log("querstr:" + querstr)
            requrll = BINANCE_API_BASE + path

        label .begin
        s = requests.Session()
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))
        try:
            response = s.request(
                method=http_method,
                url=requrll,
                headers={
                    'lang':'zh-CN'
                }
                #,data=payload  # python 字典 解析 对应Content-Type
                ,timeout=(3,2)
            )
            response.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
        except requests.RequestException as e:
            log("服务器超时重连4次失败:" + requrll +"错误："+ str(e))
            send_email("服务器超时重连3次失败:"+requrll+str(e))
            log("等待 5s ...重连... ")
            time.sleep(5)
            goto .begin
        log("requrll:" + requrll)
        json_obj ={}
        try:
            json_obj = json.loads(response.text)
        except (IndexError, IndentationError) as e1:
            log("requrll:" + requrll)
            log("resp:" + response.text)
            log("解析出错" + str(e1))
            send_email("解析出错"+response.text)
            log("等待 3s ...重试... ")
            time.sleep(3)
            goto .begin
        return json_obj
