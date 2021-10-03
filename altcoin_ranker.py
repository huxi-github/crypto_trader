from py3commas.request import Py3Commas
import json
from util import send_email,log

def get_top_5_symbol():
    p3c = Py3Commas(key='xx',
                    secret='xx'
                           ' '
                           ' '
                           ' ')

    data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/ticker/24hr"
            )
    i=0
    sorted_arry = sorted(data_arry, key = lambda i: float(i['priceChangePercent']),reverse = True)
    print('rank"\tsymbol_name ' + "\t\t\t" + 'priceChangePercent')
    top_hot_symbol={}
    for symbl_d in sorted_arry:
        if symbl_d['symbol'].endswith("BUSD") :
            if "BULL" in symbl_d['symbol'] or "DOWN" in symbl_d['symbol']: continue
            if float(symbl_d['priceChangePercent']) < 15.00 :
                    # or float(symbl_d['priceChangePercent']) < 80.00 :
                continue
            # print(str(i)+ "\t\t" + symbl_d['symbol'] + "\t\t\t\t\t" + symbl_d['priceChangePercent'])
            i = i + 1
            top_hot_symbol[symbl_d['symbol']]=symbl_d['priceChangePercent']
            if i>=3: break
    print("top 5 symbol is:" + json.dumps(top_hot_symbol))
    return top_hot_symbol

def get_top_fast_change_symbol():  #min high 和low 的差值，2.引线所占的比例  3.3min 上涨20% 可以进去

    return




if __name__ == '__main__':
    top_symbols =get_top_5_symbol()
    for (it,val) in top_symbols.items():
        print(it+"\t\t\t"+val)


##分钟内 变化率 超过 1-2% 的 筛选器。。。