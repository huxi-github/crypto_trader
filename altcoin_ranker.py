from py3commas.request import Py3Commas
import json
from util import send_email,log

def get_top_5_symbol():
    p3c = Py3Commas(key='08e94c4768d44f3a9a6f14f68f86a2a63d3dfe67f18c4f28905afad93dfadb92',
                    secret='742ce7cffb40f42883e0c454652ebad5d3ccfb125b283b92214401547ea73a'
                           'b2647f42a44e68544054ab9a70769dcfb890fdffe4a181a984287dc8d3e783'
                           'db9a7c501aaacec88af608f0e135f5c2323f921181ea2023176068396eb973'
                           '2c18c487240ec0')

    data_arry = p3c.request_binance_data(
            http_method="GET",
            path="/api/v3/ticker/24hr"
            )
    i=0
    sorted_arry = sorted(data_arry, key = lambda i: float(i['priceChangePercent']),reverse = True)
    log('rank"\tsymbol_name ' + "\t\t\t" + 'priceChangePercent')
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
            if i>=2: break
    log("top 5 symbol is:" + json.dumps(top_hot_symbol))
    return top_hot_symbol

def get_top_fast_change_symbol():  #min high 和low 的差值，2.引线所占的比例  3.3min 上涨20% 可以进去

    return




if __name__ == '__main__':
    top_symbols =get_top_5_symbol()
    for (it,val) in top_symbols.items():
        print(it+"\t\t\t"+val)


##分钟内 变化率 超过 1-2% 的 筛选器。。。