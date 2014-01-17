#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json, re, os
import sys,urlparse
import redis
import codecs
from os.path import join, exists
from settings import getRedis,suggest_url,word_path

def init_data():
    f = codecs.open(word_path,'r','utf-8')
    s = f.readlines()
    f.close()
    r = getRedis()
    try:
        for word in s:
            word=word.strip('\n')
            if word == '':
                print 'input can not be empty'
                break
            tmp = suggest_url % (word)
            r.rpush('url_list', tmp)
    except Error,e:
        print 'error'
    #print r.lpop('url_list')

def add_data():
    r = getRedis()
    try:
        tmp = suggest_url % ('连衣裙')
        r.rpush('url_list', tmp)
    except Error,e:
        print 'error'
    #print r.lpop('url_list')

def read_data():
    r = getRedis()
    print r.lpop('url_list') 

def test_data():
    from downloader import get_source
    url = "http://suggest.taobao.com/sug?code=utf-8&q=乳制品"
    page = get_source(url)
    if page is None:
        print 'page is null'
        return 
    print page 
    search = urlparse.parse_qs(url,True).get('q')[0]
    result = json.loads(page)
    for item in result.get('result'):
        print 'search:%s;word:%s;count:%s' % (search.decode('utf-8'),item[0],item[1])

if __name__=="__main__":
    #test_data()
    init_data()
    #read_data()
    #add_data()
