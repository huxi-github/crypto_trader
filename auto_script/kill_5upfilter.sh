#!/bin/sh

wait_for_process_exit() {
        local pidKilled=$1
        local begin=$(date +%s)
        local end
        while kill -9 $pidKilled > /dev/null 2>&1
        do
                echo -n "."
                sleep 1;
                end=$(date +%s)
                if [ $((end-begin)) -gt 60  ];then
                        echo -e "\nTimeout"
                        break;
                fi
        done
}

stop_service1() {
    # 查询进程ID
    local pid=$(ps -ef | grep -i "5UP_filter.py" | grep -v grep | awk '{print $2}')
        # 如果进程ID不为空
        echo "Try to kill...."
    if [[ -n $pid ]]; then
        echo "Try to kill 5UP_filter.py"
                # 杀死进程并等待进程退出  
        kill $pid && wait_for_process_exit "$pid"
    else 
        echo "5UP_filter_30min.py is killed"
    fi
}

stop_service2() {
    # 查询Java进程ID
    local pid=$(ps -ef | grep -i "5UP_filter_30min.py" | grep -v grep | awk '{print $2}')
        # 如果进程ID不为空
        
    if [[ -n $pid ]]; then
        echo "Try to kill 5UP_filter_30min.py"
                # 杀死进程并等待进程退出  
        kill $pid && wait_for_process_exit "$pid"
    else 
        echo "5UP_filter_30min.py is killed"
        #statements
    fi
}

stop_service1
stop_service2
# stop_service 5UP_filter30min.py
# # for test_api.py
# NUM0=`ps -ef | grep -i '5UP_filter.py' | grep -v "grep" | wc -l`  #查看程序进程是否存活，结果为0为不存活，非0为存活

# cd /Users/huxi/Downloads/crypto_trade_test
# if [ $NUM0 -gt 0 ]; then
#     ps -ef|grep '5UP_filter.py'|grep -v grep|cut -c 6-12|xargs kill -9
#     sleep 2s 
#     if [[ $? ]]; then
#         echo "`date +%Y%m%d-%H:%M:%S` 成功杀死运行的 5UP_filter.py进程">>./log/5UP_filter.py-crash-restart.log
#     fi
# else
#     echo "`date +%Y%m%d-%H:%M:%S` 5UP_filter.py aready died"
# fi


 

echo 按任意键继续
read -n 1
echo 继续运行