#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys,getopt
from Logger import Logger
import os
reload(sys)
sys.setdefaultencoding('utf-8')

def usage():
    print 'parameter error ...'
    print '-----------------------------'
    print '''./crawl spider 
options:
    -d path ,write output into file '''
    print '-----------------------------'

def main():
    try:
        opts,args = getopt.getopt(sys.argv[1:], 'd:')
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit()
    print 'get opt',opts,args
    global log
    for k,v in opts:
        if k == '-d':
            log = Logger(v)
            print v
            sys.stdout = log
            sys.stderr = log
        elif k == '-h':
            print 'else'
            usage()
            sys.exit()

    print 'exit!'
    print args
    #if len(args) != 1:
    #    usage()
    #    sys.exit()

    print args[0] + ' begining to crawl ... ...'
    m = __import__('scheduler')
    c = getattr(m, args[0])
    spider = c()
    spider.start()

#--------main------------------------
if __name__ == "__main__":
    import socket
    socket.setdefaulttimeout(10)
    main()

