#!/bin/sh

#安装python依赖库
echo "安装python依赖库>>>"
pip install -r ./requirements.txt
sleep 10
#配置自动保活检查
crontab -e <<*/5 0-23 * * * sh -x /Users/huxi/Downloads/crypto_trade_test/auto_script/cron_pull_up_5upfilter.sh
sleep 3