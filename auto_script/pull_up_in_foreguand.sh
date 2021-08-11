#!/bin/sh

NUM0=`ps -ef | grep -i 'test_api.py' | grep -v "grep" | wc -l`  #查看程序进程是否存活，结果为0为不存活，非0为存活

if [ $NUM0 -eq 0 ]; then
    echo "try start test_api.py.....in forguand....."
    cd /Users/huxi/Desktop/crypto
    ./venv/bin/python3 ./test_api.py
    echo "test_api.py restart date is : `date +%Y%m%d-%H:%M:%S`"        #重启进程的重启日志
else
    echo "test_api.py already running"
fi
echo
