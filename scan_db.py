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

import shelve
Frame_level= '30m'
golobal_data ="golobal_data"+Frame_level

print("初始化历史数据..."+golobal_data)
with shelve.open(golobal_data) as db:
    # db['Static']['win_count'] =

    # global sel_coin_global,Entry_pri,Static
    if 'sel_coin_global' in db:
        sel_coin_global = db['sel_coin_global']
        print(" sel_coin_global="+str(sel_coin_global))
    if 'Entry_pri' in db:
        Entry_pri = db['Entry_pri'] 
        print(" Entry_pri="+str(Entry_pri))
    if 'Static' in db:
        Static = db['Static']
        print(" Static="+str(Static))


Frame_level= '1h'
golobal_data ="golobal_data"+Frame_level
print("\n")

print("初始化历史数据..."+golobal_data)
with shelve.open(golobal_data) as db:
    # global sel_coin_global,Entry_pri,Static
    # if 'sel_coin_global' in db:
    #     sel_coin_global = db['sel_coin_global']
    #     print(" sel_coin_global="+str(sel_coin_global))
    # if 'Entry_pri' in db:
    #     Entry_pri = db['Entry_pri'] 
    #     print(" Entry_pri="+str(Entry_pri))
    # if 'Static' in db:
    #     Static = db['Static']
    #     print(" Static="+str(Static))
    for key, value in db.items():
        # print(key, value)
        print ('键{}= {}'.format(key, value))