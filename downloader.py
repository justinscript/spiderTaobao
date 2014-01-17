#!/usr/bin/env python
#-*- coding: utf-8 -*-

import StringIO
import string
import urllib, urllib2, socket, cookielib
import re, os, sys, time
import settings

def get_headers():
    headers = {
        "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.65 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language":"zh-cn,zh;q=0.5",
        "Accept-Charset":"GB2312,utf-8;q=0.7,*;q=0.7",
        "Keep-Alive":"115",
        "Connection":"keep-alive"
    }
    return headers

def get_source(source):
    time.sleep(5)
    try:
        req = urllib2.Request(source, data = urllib.urlencode(get_headers()))
    except:
        return None
    try:
        retval = urllib2.urlopen(req)
        context = retval.read().decode('utf-8').strip()
        if context is None or context == '{\"result\": []}':
            return None
    except:
        return None
    return context
