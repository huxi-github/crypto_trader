#!/bin/sh

start_service() {
    serv=$2  #$var表示以字符串形式获取var的值，类似于 get_Val(var)， serv表示定义一个变量 ，$var 是${var} 的简写
    serv_path=$1    # echo "hello" "$serv" #字符串拼接 直接 空格 或者 +
    NUM0=`ps -ef | grep -i $serv | grep -v "grep" | wc -l`  #查看程序进程是否存活，结果为0为不存活，非0为存活

    if [ $NUM0 -eq 0 ]; then
       echo -n [`date +%Y-%m-%d-%H:%M:%S`]
       echo "$serv" " is down,try start" "$serv"".........................."  #有try_start $server_name 就说明server_name 发生过重启
       cd $serv_path
       nohup python3 -u ./$serv > log/running_log/$serv.log &#记录运行日志，方便排查
       # echo "5UP_filter_30min.py(crashed) restart date is : `date +%Y%m%d-%H:%M:%S`">>./log/5UP_filter_30min.py-restart.log         #重启进程的重启日志
    else
       echo [`date +%Y-%m-%d-%H:%M:%S`]$serv "already running"
    fi
}

echo " "
echo [`date +%Y-%m-%d-%H:%M:%S`]
# start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter.py
start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter_30min_tp5_10.py
# start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter_plus_ma_day_30min.py
start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter_30min_tp5_10_white_list.py
start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter_30min_tp5_10_scan_white_skip_top_three.py
start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter_30min_tp5_sl_15_white_list_ignore_toprank.py
# start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter_30min_tp5_10_MA_grow_white_list.py
# start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter_30min_tp5_10_white_list_no_liandan.py
# start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter_30m_tp5_white_no极限_阴跌_拉伸.py
# start_service /Users/huxi/Downloads/crypto_trade_test 5UP_filter_30m_tp5_white_no极限_阴跌_拉伸_延迟1k线.py
# start_service /Users/huxi/Downloads/crypto_trade_test auto_balance_checker.py
echo 按任意键继续
read -n 1
echo 继续运行


# 让 mac/linux cron 程序自动运行该脚本【写在安装脚本里面】
# 命令行下 crontab -e 输入对应的 执行周期 
# */5 0-23 * * * sh -x /Users/huxi/Downloads/crypto_trade_test/auto_script/cron_pull_up_5upfilter.sh
# 表示 0-23 点 每个5min 执行一次