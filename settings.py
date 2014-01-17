#!/usr/bin/env python
#-*-coding:utf-8-*-
import redis
import sys
import MySQLdb
import time, datetime

# yesterday time
yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
# current day
today = datetime.datetime.now().strftime('%Y-%m-%d')
# current day 
_time_ = datetime.datetime.now().strftime('%m%d')
# taobao default login user
user=u'格物良品'.encode('gbk')
passwd='qinshuai74'
# taobao suggest url
suggest_url="http://suggest.taobao.com/sug?code=utf-8&q=%s"
#suggest_url="http://suggest.taobao.com/sug?code=utf-8&bucketid=9&q=%s"
# taobao suggest word path
word_path="/tmp/_word_"

def getRedis(db=0):
    return redis.StrictRedis(host='localhost', port=6379, db=db)

def getMysql():
    return MySQLdb.connect(host='192.168.1.100',\
            user='dev',passwd='dev1234',db="my_db",port=3306,charset="utf8")

def get_Maps(cfg='./maps.cfg'):
    map_file = open(cfg, "r")
    str = map_file.read()
    map_file.close()
    try:
        d = eval(str)
    except:
        print 'The Maps config is error! Please check it.'
        sys.exit()
    return d
