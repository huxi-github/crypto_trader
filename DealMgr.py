import sqlite3
from datetime import datetime

class DEALMGR:

    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS DEAL (
                            id INTEGER PRIMARY KEY,
                            symbol TEXT,
                            entry_time TEXT,
                            entry_price REAL,
                            exit_time TEXT,
                            exit_price REAL,
                            PNL_per REAL,
                            deal_duration TEXT,
                            exit_reason TEXT,
                            status TEXT
                        )''')
        
        self.conn.commit()

    def create_deal(self, symbol, entry_price):
        entry_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        exit_time = None
        deal_duration = None
        exit_price = None
        status = 'open'
        self.cursor.execute("INSERT INTO DEAL (symbol, entry_time, entry_price, exit_time, exit_price, deal_duration,status) VALUES (?, ?, ?, ?, ?, ?,?)", (symbol, entry_time, entry_price, exit_time, exit_price,deal_duration, status))
        self.conn.commit()

    def close_deal(self, symbol, exit_price, exit_reason ='stop_limit'):
        exit_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        record = self.cursor.execute("SELECT * FROM DEAL WHERE symbol =? and status =?",(symbol,'open')).fetchone()
        entry_time = record[2]
        entry_price = record[3]
        print("entry_time:"+str(entry_time))
        deal_duration = str(datetime.now() - datetime.strptime(entry_time,'%Y-%m-%d %H:%M:%S')).split('.')[0]
        print("deal_duration:"+str(deal_duration))
        PNL_per = "{:.2f}".format((exit_price - entry_price)/entry_price*100)
        print("PNL_per:"+str(PNL_per))
        print("entry_price:"+str(entry_price))
        print("exit_reason:"+str(exit_reason))

        status = 'closed'
        # deal_duration = None
        self.cursor.execute("UPDATE DEAL SET exit_price=?, exit_time=?, deal_duration=?,status=?,PNL_per=?,exit_reason=? WHERE symbol=? and status=?", (exit_price, exit_time, deal_duration,status, PNL_per,exit_reason,symbol,'open'))
        self.conn.commit()

    def get_all_unclosed_deal(self):
        self.cursor.execute("SELECT * FROM DEAL WHERE status ='open' ")
        return self.cursor.fetchall()

    def get_all_closed_deal(self):
        self.cursor.execute("SELECT * FROM DEAL WHERE status ='closed' ")
        return self.cursor.fetchall()

    def get_all_deal(self):
        self.cursor.execute("SELECT * FROM DEAL")
        return self.cursor.fetchall()

if __name__ == '__main__':
    Deal = DEALMGR('db_file/sqlite/example.db')
    symbol = 'BTCUSDT'
    entry_price = 50000.00
    print("------create_a_deal------")
    Deal.create_deal(symbol,entry_price)
    print("------get_all_deal------")
    deals = Deal.get_all_deal()
    print(deals)

    print("------get_all_unclosed_deal------")
    deals = Deal.get_all_unclosed_deal()
    print(deals)

    print("------close_deal------")
    Deal.close_deal("BTCUSDT",67000,"market_sell")
    # deals = Deal.get_all_closed_deal()
    # print(deals)

