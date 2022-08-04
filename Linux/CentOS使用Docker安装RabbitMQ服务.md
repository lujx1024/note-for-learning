---
title: CentOS使用Docker安装RabbitMQ服务
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---
# 概述
本篇笔记用于记录使用`Docker`容器在`CentOS`系统(**适用于所有Linux发行版**)快速安装使用RabbitMQ服务。
**当前环境**：
- CentOS 7 64位
- Docker 19.3

# 安装部署
## 拉取镜像

```
#指定版本，该版本包含了web控制页面
docker pull rabbitmq:management
```

## 创建并启动容器

```
#方式一：默认guest 用户，密码也是 guest
docker run -d --hostname my-rabbit --name rabbit -p 15672:15672 -p 5672:5672 rabbitmq:management

#方式二：设置用户名和密码
docker run -d --hostname my-rabbit --name rabbit -e RABBITMQ_DEFAULT_USER=user -e RABBITMQ_DEFAULT_PASS=password -p 15672:15672 -p 5672:5672 rabbitmq:management
```

## 访问服务

```
# 查询当前所有的容器
docker ps -a
```

|  CONTAINER  ID  |  IMAGE    |  COMMAND   |   CREATED   |  STATUS    |  PORTS    |  NAMES   |
| ----------------------- | ------------- | ------------------ | ------------------ | -------------- | -------------- | ------------- |
|   466131dc8ab6  |   rabbitmq:management  |  "docker-entrypoint.s…"   |   43 hours ago  |  Up 43 hours   | 4369/tcp, 5671/tcp, 0.0.0.0:5672->5672/tcp, 15671/tcp, 15691-15692/tcp, 25672/tcp, 0.0.0.0:15672->15672/tcp    |   rabbit  |

查询容器状态，如容器未启动，先启动容器:
```
# 使用container name启动容器
docker start rqbbit

# 使用container ID启动容器
docker start 466131dc8ab6 
```
访问管理页面
```
http://localhost:15672/
```

# 参考链接
- https://hub.docker.com/_/rabbitmq?tab=tags
- https://www.cnblogs.com/angelyan/p/11218260.html

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。