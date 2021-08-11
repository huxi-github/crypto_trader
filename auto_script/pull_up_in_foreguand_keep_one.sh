#!/bin/sh

NUM0=`ps -ef | grep -i 'test_api.py' | grep -v "grep" | wc -l`  #查看程序进程是否存活，结果为0为不存活，非0为存活

if [ $NUM0 -gt 1 ]; then  #启动前先检查，金杀死所有 存在的进程
    ps -ef|grep 'test_api.py'|grep -v grep|cut -c 6-12|xargs kill -9
    if [[ $? ]]; then
        echo "成功杀死所有在运行的test_api.py老进程"
    fi
fi

NUM1=`ps -ef | grep -i 'test_api.py' | grep -v "grep" | wc -l`

if [ $NUM1 -eq 0 ]; then
    echo "尝试启动新进程 test_api.py.....foreguand....."
    cd /Users/huxi/Desktop/crypto
    ./venv/bin/python3 ./test_api.py
    echo "test_api.py 启动成功 date is : `date +%Y%m%d-%H:%M:%S`"        #重启进程的重启日志
fi
