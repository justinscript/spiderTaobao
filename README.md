分布式定向抓取集群
------------------------------------------------------------------------------------------------------------------------
一个完整的抓取数据流：
1：用户提供种子URL
2：种子URL进入linkbase中新URL队列中
3：调度模块选取url进入到抓取模块的待抓取队列中
4：抓取模块读取站点的配置文件，按照执行的频率进行抓取
5：抓取的结果返回到pipeline接口中，并完成连接的抽取
6：新发现的连接在linkbase里面进行dedup，并push到linkbase的新URL模块里面
7：调度模块选取url进入抓取模块的待抓取队列，goto 4
8：end

目前实现功能
-------------
1. 多线程下载,线程数可配置。
2. 无需修改代码，按照规则添加配置就可以完成页面抽取、入库。
3. 利用Redis的list作为抓取队列，zset作为已抓取集合。
4. 支持分布式部署多个爬虫，Redis作为核心，mysql为存储,当然redis/mysql自身拥有各自的扩展方案。

INSTALL
========
确认安装Python2.7及依赖库: 
        MySQLdb: http://sourceforge.net/projects/mysql-python/
        python客户端 redis: git clone https://github.com/andymccurdy/redis-py.git 
        远程服务端 redis: wget http://redis.googlecode.com/files/redis-1.2.6.tar.gz
        lxml: wget --no-check-certificate http://pypi.python.org/packages/source/l/lxml/lxml-3.0.1.tar.gz

settings.py
-------------
配置Redis,mysql的连接参数
配置maps.cfg路径位置

部署
========
首先确认redis和mysql服务是否已启动并可用，然后执行：
1.启动redis服务 redis-server;启动mysql服务,创建数据库表
2.初始化redis待爬取数据的url
3.启动脚本crawl.py,test_spider 参数用来测试脚本环境是否正常,roach 参数是启动爬虫， -d 是日志路径
    python crawl.py roach -d /home/admin/spider/ > /tmp/log 2>&1 &
4.爬虫脚本启动后，会长时间爬取淘宝suggest数据，可通过日志和数据库查看

::
    ./crawl spider_name
    options:
        -d ./logs 可将输出写入指定文件夹的日志中
