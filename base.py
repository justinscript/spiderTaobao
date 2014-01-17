#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import sys
import re
import MySQLdb
import threading
from settings import getMysql
from downloader import get_source

global url_maps
url_maps = {}

class BaseDb():
    db = None
    table = "m_word_source"
    ks = "GMT_CREATE,GMT_MODIFIED,WORD_SOURCE,WORD,SEARCH_COUNT,WORD_DATE"
    def connectdb(self):
        try:
            self.db = getMysql()
            print 'connect to the dbserver !'
        except:
            print ":failed connected to db!"
        return self.db
    
    def execsql(self,sql):
        cursor=self.db.cursor()
        try:
            cursor.execute(sql)
            self.db.commit()
        except:
            info=sys.exc_info()
            print info[0],":---",info[1]
            self.connectdb()
            return False
    
        cursor.close()
        return True

    def __del__(self):
        self.db.close()

    def escapeString(self, s):
        if s is None:
            return 'NULL'
        elif isinstance(s, basestring):
            return '"%s"' % (s.replace('\\','\\\\').replace('"','\\"'))
        else:
            return str(s)
    #insert into m_word_source(GMT_CREATE,GMT_MODIFIED,WORD_SOURCE,WORD,SEARCH_COUNT,WORD_DATE) values(now(),now(),'连衣裙', '连衣裙 女', 2345,now());
    def sql_insert(self,search,word,count):
        vs = 'now(),now(),"%s","%s",%s,now()' % (search,word,count)
        sql = 'insert into %s (%s) values (%s)' % (self.table,self.ks,vs)
        return sql

    def sql_update(self,word,count):
        sql = 'update %s set count=%s where word="%s"' % (self.table,count,word)
        return sql

    def query(self, sql, record_callback):
        cur = self.db.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        cur.execute(sql)
        numrows = int(cur.rowcount)
        for i in range(numrows):
            fields = cur.fetchone()
            record_callback(fields)

class BaseParse():
    html = None
    item = {}
    def findrules(self,url):
        """Return the corresponding selection rules"""
        for k,v in url_maps.items():
            if re.match(k, url):
                return v
        return None

class spider_thread(threading.Thread):
    def __init__(self, threadName, list, pipename):
        threading.Thread.__init__(self, name = threadName)
        self.url_list = list['url']
        m = __import__('pipeline')
        c = getattr(m, pipename)
        self.pipeline = c(list)
    def run(self):
        while True:
            if self.url_list.empty():
                time.sleep(3)
                break
            url = self.url_list.pop()
            if not url:
                continue
            print '['+self.getName()+']'+'[pop]'+str(self.url_list.len())+ "[get]"+url
            page = get_source(url)
            if page == None:
                print '['+self.getName()+']'+'[push]'+str(self.url_list.len())+ "[get source error:]"+url
                if '&bucketid=7' not in url:
                    self.url_list.push(url + '&bucketid=7')
                continue
            if not self.pipeline.parse(url, page, self.getName()):
                print '['+self.getName()+']'+'[push]'+str(self.url_list.len())+ "[parse error:]"+url
                #self.url_list.push(url)

class BaseSpider():
    rules = [ ] 
    def __init__(self):
        self.Rules()
    def __Rules(self):
        pass
    def AddRules(self, list, pipe, name='Unkonwn', threadsize=1):
        """Add extraction rules"""
        self.rules += [{'name':name,'list':list,'pipe':pipe, 'threadsize':threadsize},]

    def scheduling(self):
        pass

    def start(self):
        for ru in self.rules:
            threadList = []
            for i in xrange(ru['threadsize']):
                threads = spider_thread(ru['name']+str(i), ru['list'], ru['pipe'])
                threadList.append(threads)
            for i in threadList:
                i.setDaemon(True)
                i.start()
        try:
            self.scheduling()
        except:
            print 'quit.'
