# # for on_line_updater.py
# NUM0=`ps -ef | grep -i 'on_line_updater.py' | grep -v "grep" | wc -l`  #查看程序进程是否存活，结果为0为不存活，非0为存活

# if [ $NUM0 -eq 0 ]; then
#     echo "try start on_line_updater.py.........."
#     cd /Users/huxi/Desktop/crypto
#     nohup ./venv/bin/python3 ./on_line_updater.py>./log/running-log/on_line_updater_back_log_`date +%Y%m%d`.txt  &            #后台启动程序，作为daemon(每小时内运行的日志->写入到一个文件)，不会阻塞终端
#     echo "on_line_updater.py start date is : `date +%Y%m%d-%H:%M:%S`">>./log/on_line_updater.py-start.log         #启动进程的重启日志
# else
#     echo "on_line_updater.py already running"
# fi


# # for validate_finder.py
# NUM0=`ps -ef | grep -i 'validate_finder.py' | grep -v "grep" | wc -l`  #查看程序进程是否存活，结果为0为不存活，非0为存活

# if [ $NUM0 -eq 0 ]; then
#     echo "try start validate_finder.py.........."
#     cd /Users/huxi/Desktop/crypto
#     nohup ./venv/bin/python3 ./validate_finder.py>./log/running-log/validate_finder_back_log_`date +%Y%m%d`.txt  &            #后台启动程序，作为daemon(每小时内运行的日志->写入到一个文件)，不会阻塞终端
#     echo "validate_finder.py start date is : `date +%Y%m%d-%H:%M:%S`">>./log/validate_finder.py-start.log         #启动进程的重启日志
# else
#     echo "validate_finder.py already running"
# fi
