一.提前准备
1.选择程序的，日志目录，否则报错，报错日志在daemon.log中查看
2.将new_msg_id_folder 目录和文件 cp到 守护进程运行目录

二.依赖
1.安装python3
2.安装项目依赖 pip install -r requirements.txt

三.运行方法

四.保活配置
命令行crontab -e 输入对应的 添加如下配置 
例如:*/5 0-23 * * * sh -x /Users/huxi/Downloads/crypto_trade_test/auto_script/cron_pull_up_5upfilter.sh

三.部署mac 可以通过paral win 环境传输文件到服务器

