#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import urlparse
import re,json,os
import format
from lxml import etree
from base import BaseParse
from base import BaseDb
from settings import getRedis,suggest_url

class Parse_json(BaseParse):
    def __init__(self,list):
        self.parser = etree.HTMLParser(encoding = 'utf-8')
        self.db = BaseDb()
        self.db.connectdb()
        self.url_list = list['url']
        self.url_set = list['url_set']

    def parse(self, url, page,threadName):
        search = urlparse.parse_qs(url,True).get('q')[0]
        try:
            # The non-standard json string, the regular process standardization
            re_item = re.compile(r'(?<=[{,])\w+')
            page = re_item.sub("\"\g<0>\"", page)
            result = json.loads(page)
        except:
            print 'json parse error,search:%s,page:%s' % (search,page)
            return True
        for item in result.get('result'):
            if (item is None) or (item[0] is None) or item[0] == '':
                continue
            word=format.strip_tags(item[0])
            #print 'search:%s;word:%s;count:%s' % (search.decode('utf-8'),item[0],item[1])
            try:
                self.save2db(search.decode('utf-8'),word,item[1])
            except:
                print 'save to database faild,search word:%s' % search
            self.add2redis(word)
            return True
    
    def save2db(self,search,word,count):
        sql = self.db.sql_insert(search,word,count)
        if self.db.execsql(sql):
            print 'save word:【%s】 to database,success!' % word
        else:
            print 'save word:【%s】 to database,faild' % word
    
    def add2redis(self,word):
        #r = getRedis()
        try:
            s=format.extract(word)
            for w in s:
                tmp = suggest_url % w
                #r.rpush('url_list', tmp)
                self.url_list.push(tmp)
        except:
            print 'put to redis error,word:%s' % word       
