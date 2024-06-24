#!/bin/sh

start_service() {
    serv=$2  #$var表示以字符串形式获取var的值，类似于 get_Val(var)， serv表示定义一个变量 ，$var 是${var} 的简写
    serv_path=$1    # echo "hello" "$serv" #字符串拼接 直接 空格 或者 +
    NUM0=`ps -ef | grep -i $serv | grep -v "grep" | wc -l`  #查看程序进程是否存活，结果为0为不存活，非0为存活

    if [ $NUM0 -eq 0 ]; then
       echo [`date +%Y-%m-%d-%H:%M:%S`]"$serv" " is down,try start" "$serv"".........................."  #有try_start $server_name 就说明server_name 发生过重启
       cd $serv_path
       # cmd=python3 ./$serv>./log/running-log/$serv`date +%Y%m%d-%H:%M:%S`.txt
       cmd="python3 ./$serv" #现在每个后台进程都有自己的服务日志,不用记录标志输出
       python3 ./$serv
       sleep 2 
       echo $cmd              #后台启动程序，作为daemon
    else
       echo [`date +%Y-%m-%d-%H:%M:%S`]$serv "already running"
    fi
}


# echo -n [`date +%Y-%m-%d-%H:%M:%S`]
start_service /Users/huxi/Downloads/crypto_trade_test open_the_real_bot.py
# start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter_30min_tp5_10_white_list.py

echo [`date +%Y-%m-%d-%H:%M:%S`]按任意键继续
# read -n 1
echo [`date +%Y-%m-%d-%H:%M:%S`]继续运行
# echo " "
