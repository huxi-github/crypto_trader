#!/bin/sh


# NUM0=`ps -ef | grep -i 'test_api.py' | grep -v "grep" | wc -l`  #查看程序进程是否存活，结果为0为不存活，非0为存活

# if [ $NUM0 -eq 0 ]; then
#    echo "try start test_api.py.........."
#    cd /Users/huxi/Desktop/crypto
#    nohup ./venv/bin/python3 ./test_api.py>./log/running-log/back_log_`date +%Y%m%d-%H:%M:%S`.txt  &              #后台启动程序，作为daemon
#    echo "test_api.py(crashed) restart date is : `date +%Y%m%d-%H:%M:%S`">>./log/test_api.py-crash-restart.log         #重启进程的重启日志
# else
#    echo "test_api.py already running"
# fi

# for auto_balance_adder.py
# NUM0=`ps -ef | grep -i 'auto_balance_adder.py' | grep -v "grep" | wc -l`  #查看程序进程是否存活，结果为0为不存活，非0为存活

# if [ $NUM0 -eq 0 ]; then
#    echo "try start auto_balance_adder.py.........."
#    cd /Users/huxi/Desktop/crypto
#    nohup ./venv/bin/python3 ./auto_balance_adder.py>./log/running-log/balance_adder_start_log.txt  &              #后台启动程序，作为daemon
#    echo "auto_balance_adder.py(crashed) restart date is : `date +%Y%m%d-%H:%M:%S`">>./log/auto_balance_adder.py-crash-restart.log         #重启进程的重启日志
# else
#    echo "auto_balance_adder.py already running"
# fi
