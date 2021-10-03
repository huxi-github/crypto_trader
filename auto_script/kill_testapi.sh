#!/bin/sh

# for test_api.py
NUM0=`ps -ef | grep -i 'test_api.py' | grep -v "grep" | wc -l`  #查看程序进程是否存活，结果为0为不存活，非0为存活

cd /Users/huxi/Desktop/crypto
if [ $NUM0 -gt 0 ]; then
    ps -ef|grep 'test_api.py'|grep -v grep|cut -c 6-12|xargs kill -9
    if [[ $? ]]; then
        echo "`date +%Y%m%d-%H:%M:%S` 周五休息市成功杀死运行的test_api.py进程">>./log/test_api.py-crash-restart.log
    fi
else
    echo "`date +%Y%m%d-%H:%M:%S` 周五 test_api.py aready died">>./log/test_api.py-crash-restart.log
fi