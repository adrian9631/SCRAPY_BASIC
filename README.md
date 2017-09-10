# SCRAPY_BASIC（SCRAPY基础设置）  
Including the basic settings about the databse storage，the duplicate filter，the tor proxy and so forth  
  
  

## Overview （项目概述）
本项目建立在scrapy框架基础上，编写了多个插件分别实现了**反爬**，**去重**，**存储**等功能。反爬处理包括随机ua的生成和基于tor代理的动态IP实现（中国内陆需要翻墙），URL及数据去重基于redis数据库并利用布隆过滤器（Bloom Filter）进行处理，使用mongodb数据库做数据存储。  

--------
## Requirements （项目环境）  
#### 1.安装配置shadowsocks翻墙
请参考https://github.com/shadowsocks/shadowsocks-windows （在本地1080端口运行ss服务)  

#### 2.导入ua表至mysql本地数据库  
    $ mysql -u username -p database < ua.sql  
    
#### 3.安装配置Tor代理，Stem（调度库）和 polipo（HTTP代理）  
利用apt进行安装:  

    $ apt-get install tor python-stem polipo  

用tor命令hash加密密码:  
    
    $ tor --hash-password secretPassword   

将加密密码，端口号，代理地址，认证信息填写至`/etc/tor/torrc`:  
    
    ControlPort 9051
    HashedControlPassword  16:4BACA186EEB773696065AF69D10BFEA474970DCF5B8A860F33D052B686  
    Socks5Proxy 127.0.0.1:1080  
    CookieAuthentication 1  

将代理地址填写至`/etc/polipo/config`:  
    
    socksParentProxy = localhost:9050  

重新运行tor，polipo代理:  

    $ service tor restart
    $ service polipo restart
    
#### 4.启动mysql，redis，mongodb数据库服务  
数据库的安装配置请详情参考官网  
使用pip安装python的数据库依赖包：  
    
    $ pip install MySQL-python redis pymongo  
    
在`redis/src`目录下：  

    $ .redis-server ../redis.conf

启动mongodb数据库：  
    
    $ mongod --auth

启动mysql数据库：  
    
    $ service mysql start

----------
## Configuration （文件设置）
#### 只需在项目中的 `settings.py` 进行设置
#### 1.MYSQL SETTINGS
填写本地**MYSQL**数据库的**地址**，**用户名**，**密码**以及**数据库名**（本地MYSQL数据库存储**User-Agent Table**，用于**随机UA（Random UA）**）

    MYSQL_HOST        =  # 'localhost' 
    MYSQL_USER        =  # 'username'  
    MYSQL_PASSWORD    =  # 'password'  
    MYSQL_DATABASE    =  # 'databasename'
    
#### 2.REDIS SETTINGS
填写本地**REDIS**数据库的**地址**，**端口号**，**密码**以及**数据库号**（本地REDIS数据库用于**去重（DUPLICATE）**）

    REDIS_HOST        =  # '127.0.0.1'  
    REDIS_PORT        =  # '6379'  
    REDIS_PASSWORD    =  # 'password'  
    REDIS_DB1         =  # 1                  #DUPLICATE URLS  
    REDIS_DB2         =  # 2                  #DUPLICATE ITEMS
    
#### 3.MONGODB SETTINGS
填写本地**MONGODB**数据库的**用户名**，**密码**，**地址**，**端口号**以及**数据库名**（本地REDIS数据库用于**存储（STORAGE）**）

    MONGO_URI         =  # 'mongodb://usrname:password@127.0.0.1:27017'
    MONGO_DATABASE    =  # 'databasename'

#### 4.TOR SETTINGS
填写TOR服务的**地址**，**密码**，，**端口号**以及**每次变更IP的请求数**（TOR服务用于**动态IP（Random IP Addresses）**）

    HTTP_PROXY        =  # 'http://127.0.0.1:8123'
    AUTH_PASSWORD     =  # 'secretPassword'
    CONTROL_PORT      =  # 9051
    MAX_REQ_PER_IP    =  # 80                 # Number of HTTP request before the IP change

#### 5.DUPLICATE SAVE SETTINGS  
填写**URL地址**或者利用**正则表达式**进行匹配（启动REDIS去重后，用于**保留部分需要重复发送请求的URL地址**）

    SPECIAL_URLS     = # ['http://music.163.com/weapi/v1/resource/comments/R_SO_4_185807/?csrf_token=']  
    SPECIAL_URLS_RES = # [ur'http:\/\/music\.163\.com\/weapi\/v1\/resource\/comments\/R_SO_4_\d+\/\?csrf_token=']
    
#### 6.Enable or disable downloader middlewares
中间插件执行顺序由上往下分别是**URL去重**，**随机UA**，**动态IP**（加“#”注释即可停用插件）  

    DOWNLOADER_MIDDLEWARES = {  
    #'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':400,  
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware':None,  
    'Basic.middlewares.IngoreRequestMiddleware':310,  
    'Basic.middlewares.RandomUserAgentMiddleware':400,  
    'Basic.middlewares.TorProxyMiddleware': 410,  
    }

#### 7.Configure item pipelines
下载插件执行顺序由上往下分别是**ITEM去重**，**ITEM存储**（加“#”注释即可停用插件）  

    ITEM_PIPELINES = {  
    'Basic.pipelines.RedisDuplicatePipeline': 100,  
    'Basic.pipelines.MongodbPipeline': 300,  
     }


------------
## Usage （运行测试）
1.修改项目信息Target :  
     
    $ vi scrapy.cfg (vi settings.py)  
在vi编辑器工作栏下  
    
    :%s/Basic/Target/g  

2.运行，测试IP ：  

    $ scrapy crawl IPtester  

3.截图：  
  
![image](https://github.com/adrianyoung/SCRAPY_BASIC/blob/master/example.png?raw=true)
    

> 关于我，欢迎联系  
  微信：[yd0301]() 邮箱：yd0301@outlook.com
  
