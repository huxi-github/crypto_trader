# import shelve

# import shelve

# with shelve.open('data') as db:
#     db['username'] = 12345678
#     db['password'] = 98765432

# with shelve.open('data') as db:
#     username = db['username']
#     password = db['password']

# print(f'账号为：{username}')
# print(f'密码为：{password}')


#### golobal_data.db 数据库展示
import shelve 
Frame_level= '1h'
golobal_data ="golobal_data"+Frame_level

print("初始化历史数据..."+golobal_data)
with shelve.open(golobal_data) as db:
    for key, value in db.items():
        print ('键 {} = {}'.format(key, value))

    # db['Entry_pri'] ={}
    # db['Last_Entry_TICKDate']={}
    # db['sel_coin_global']=[] 
    # db['lose_count']=0
    # db['win_count']=0
    # db['Staic']={"inital_dollers":10000,"current_balance":10000,"win_count":0,"lose_count":0}


#### golobal_data1h.db 数据库展示,数据库清零
Frame_level= '30m'
golobal_data ="golobal_data"+Frame_level
print("\n")

print("初始化历史数据..."+golobal_data)
with shelve.open(golobal_data) as db:
    for key, value in db.items():
        print ('键 {} = {}'.format(key, value))

    # db['Entry_pri'] ={}
    # db['Last_Entry_TICKDate']={}
    # db['sel_coin_global']=[] 
    # db['lose_count']=0
    # db['win_count']=0
    # db['Staic']={"inital_dollers":10000,"current_balance":10000,"win_count":0,"lose_count":0}

