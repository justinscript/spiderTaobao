#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
import re,json,os
from HTMLParser import HTMLParser

def extract(word):
    s=set()
    word=word.strip()
    word=word.replace('%20','')
    s.add(word)
    s.add(extract_word(word))
    s.add(cutword(word))
    s.add(addblank(word))
    return s
    #for w in s:
    #    print w

def extract_word(word):
    return addblank(cutword(word))    

# 截取中文一个字符,从后面开始截断
def cutword(word):
    w = word.decode('utf-8')
    l = len(w)
    s = w[0:l-1].encode('utf-8')
    return s

# add blank to word
def addblank(word):
    return word + "%20"

class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)
 
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#if __name__=="__main__":
#    extract('连衣裙%20')
