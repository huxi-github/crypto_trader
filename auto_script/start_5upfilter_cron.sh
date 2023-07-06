#!/bin/sh

start_service() {
    serv=$2  #$var表示以字符串形式获取var的值，类似于 get_Val(var)， serv表示定义一个变量 ，$var 是${var} 的简写
    serv_path=$1    # echo "hello" "$serv" #字符串拼接 直接 空格 或者 +
    NUM0=`ps -ef | grep -i $serv | grep -v "grep" | wc -l`  #查看程序进程是否存活，结果为0为不存活，非0为存活

    if [ $NUM0 -eq 0 ]; then
       echo "try start" "$serv"".........................."
       cd $serv_path
       nohup python3 ./$serv>./log/running-log/$serv`date +%Y%m%d-%H:%M:%S`.txt  &              #后台启动程序，作为daemon
       # echo "5UP_filter_30min.py(crashed) restart date is : `date +%Y%m%d-%H:%M:%S`">>./log/5UP_filter_30min.py-restart.log         #重启进程的重启日志
    else
       echo $serv "already running"
    fi
}

# start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter.py
start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter_30min.py
start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter_plus_ma_day_30min.py
start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter_30min_tp5_10_white_list.py
start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter_30min_tp5_10_MA_grow_white_list.py
echo 按任意键继续
# read -n 1
echo 继续运行


# 让 mac/linux cron 程序自动运行该脚本【写在安装脚本里面】
# 命令行下 crontab -e 输入对应的 执行周期 
# */5 0-23 * * * sh -x /Users/huxi/Downloads/crypto_trade_test/auto_script/cron_pull_up_5upfilter.sh
# 表示 0-23 点 每个5min 执行一次