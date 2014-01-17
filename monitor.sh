#!/bin/bash

basedir="$( cd "$( dirname "$0" )" && pwd )"
ps_status="alive"
full_class_name=""

cd $basedir
echo $basedir

start_spider() {
    /usr/bin/python crawl.py roach -d /home/admin/spider/ >/tmp/suggest.log
}

ps_spider() {
    count=`ps axu|grep "python crawl.py"|grep -v grep|wc -l`
    if [ $count -gt 0 ]; then
        ps_status="alive"
    else
        ps_status="unalive"
    fi
}

restart_spider() {
    sleep 10
    ps_spider
    if [ $ps_status != "alive" ]; then
        start_spider
    fi
}

ps_spider
echo $ps_status
if [ $ps_status == "alive"  ]; then
    echo 'status,alive'
fi
#start_spider
restart_spider
