import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem
import pandas as pd
import shelve
import datetime
import sqlite3

conn = sqlite3.connect("trade_list_30m_sqlite3.db")
# 示例持仓数据
data = {
    '股票代码': ['AAPL', 'GOOGL', 'MSFT'],
}



def get_Entry_Date(sel,Last_Entry_Date):
    Entry_date = []
    for it in sel:
        # print(type(Last_Entry_Date[it]))
        Entry_date.append(Last_Entry_Date[it]+datetime.timedelta(hours=8.5))
    return Entry_date

def get_time_last(data):
    data_t =[]
    for it_time in data:
        duration = datetime.datetime.now() -it_time
        if duration.days ==0:
            data_t.append(str(round(duration.seconds/3600,1))+ "小时" )
        else:
            data_t.append(str(duration.days)+"天" +str(round(duration.seconds/3600,1))+ "小时" )
    return data_t

def change_formate(data):
    data_t =[]
    for it_time in data:
        duration = it_time
        print(duration)
        if duration.days ==0:
            td=str(duration).replace("0 days","0天")
            data_t.append(':'.join(str(td).split(':')[:2]))
        else:
            td=str(duration).replace("days","天")
            data_t.append(':'.join(str(td).split(':')[:2]))
    return data_t


    
print("初始化数据...")

df = pd.read_sql("SELECT symbol as 股票代码, entry_price as 入场价格, entry_time as 入场时间, exit_time as 出场时间, exit_price as 出场价格  FROM DEAL WHERE status ='closed' ", conn) #
print(df)
# 计算持股盈亏
# df['当前价格'] = [160.50, 2600.75, 310.25]
df['盈亏%'] = round(100*(df['出场价格'] - df['入场价格'])/df['入场价格'],3)
df['入场价格'] = round(df['入场价格'],3)
df['出场价格'] = round(df['出场价格'],3)


# 去除字符串中的前后空格
df['入场时间'] = df['入场时间'].str.strip()
df['出场时间'] = df['出场时间'].str.strip()

pd_last=  pd.to_datetime(df['出场时间'], format='%Y-%m-%d %H:%M:%S') -pd.to_datetime(df['入场时间'], format='%Y-%m-%d %H:%M:%S')
df['持续']= change_formate(pd_last)

# 创建 GUI 窗口并展示持仓和盈亏情况
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('历史交易记录')
        self.setGeometry(100, 100, 720, 400)

        table = QTableWidget(self)
        table.setColumnCount(len(df.columns))
        table.setRowCount(len(df))

        # 设置表头
        table.setHorizontalHeaderLabels(df.columns)

        # 填充数据
        for i, row in df.iterrows():
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                table.setItem(i, j, item)

        self.setCentralWidget(table)

def ShowList():
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    # sys.exit(app.exec_())
    app.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
