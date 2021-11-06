---
title: Python使用Redis收发数据
tags: Python,Redis
renderNumberedHeading: true
grammar_cjkRuby: true
---

# Windows安装Redis

## 下载
下载链接 `https://github.com/MicrosoftArchive/redis/releases`,下载压缩包后，解压到某一位置，例如 `D:\redis\`

## 服务启动与连接

### 启动Redis临时服务
打开cmd，进入到刚才解压到的目录，启动临时服务：
`redis-server.exe redis.windows.conf `

> 注：通过这个命令，会创建Redis临时服务，不会在window Service列表出现Redis服务名称和状态，此窗口关闭，服务会自动关闭。

### 客户端连接

打开另一个cmd窗口，客户端调用：`redis-cli.exe -h 127.0.0.1 -p 6379`

## (选用) Redis自定义windows服务安装

1. 进入Redis安装包目录，安装服务：`redis-server.exe --service-install redis.windows.conf --service-name redisserver1 --loglevel verbose`


2. win+r -> services.msc,可以看到服务安装成功，服务名 :  `redisserver1`

其他相关指令 ：
- 安装服务：`redis-server.exe --service-install redis.windows.conf --service-name redisserver1 --loglevel verbose`
- 启动服务：`redis-server.exe  --service-start --service-name redisserver1`
- 停止服务：`redis-server.exe  --service-stop --service-name redisserver1`
- 卸载服务：`redis-server.exe  --service-uninstall--service-name redisserver1`

# Python环境安装Redis依赖

`pip  install redis`

# Python 推送数据

方法：`set(name, value, ex=None, px=None, nx=False, xx=False)`

在Redis中设置值，默认，不存在则创建，存在则修改
参数：
- ex，过期时间（秒）
- px，过期时间（毫秒）
- nx，如果设置为True，则只有name不存在时，当前set操作才执行
- xx，如果设置为True，则只有name存在时，当前set操作才执行


```
redis_host = '192.168.6.5'
redis_port = 6379
# host是redis主机,redis默认端口是6379
pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)
redis_client = Redis(connection_pool=pool)

# 更新redis数据，key、msg 分别是键、值
redis_client.set(name=key, value=msg)
```

# Python 获取数据


示例代码 : 
```
redis_host = '192.168.6.5'
redis_port = 6379
# host是redis主机,redis默认端口是6379
pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)
redis_client = Redis(connection_pool=pool)

# 更新redis数据，key、msg 分别是键、值
redis_client.get(key)
```



欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。