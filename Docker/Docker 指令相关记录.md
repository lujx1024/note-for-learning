---
title: Docker 指令相关记录
tags: Docker,指令,Container
renderNumberedHeading: true
grammar_cjkRuby: true
---

[TOC]
# 镜像


## 搜索镜像
```
docker search wordpress
```
## 拉取镜像
```
docker pull wordpress
# 或
docker image pull wordpress
# 拉取指定版本镜像
docker image pull wordpress:version
```
##  查看镜像
```
docker image ls
# 或
docker images
```
## 删除镜像(140为镜像ID)
```
docker image rm 140
```

## 镜像保存与导入
```
# 镜像导出
docker image save centos:latest -o my_centos.image
# 镜像导入
docker image load -i my_centos.image 
```



# 容器(container)相关

## 运行容器(以nginx为例)
```
docker container run nginx 
# 或
docker run nginx
```
##  查看当前所有容器
```
# 
# 包括已运行和未运行的container,去掉 -a 则只显示已运行的容器
docker container ls -a
# 或简写为（-a参数同上）
docker ps -a
# 只显示 container_id
docker ps -aq
```
## 停止容器
```
# 停止单个容器
# b7 为container_id的前两位
docker container stop b7
# 或简写为
docker stop b7

# 批量停止所有正在运行的容器
docker container stop $(docker container ls -q)
```
## 删除容器
```
# 删除单个容器
# b7 为container_id的前两位
docker container rm b7
# 或简写为
docker rm b7

# 批量删除所有容器
docker container stop $(docker container ls -aq)
```

## 容器端口映射
以nginx为例，添加`-p local_port:container_port`，即可通过本地端口访问容器中的nginx,
```
# 将本地8080端口映射到容器中的80端口
docker container run -p 8080:80 nginx 
```

此时访问`http://127.0.0.1:8080`即可访问容器中的nginx首页


## 交互模式与后台模式
以Ubuntu为例，创建可交互的容器
```
# 以attach模式启动容器，仅做示例使用
# 参数解释: i 表示interactive,可交互 , t 表示terminal，终端 
docker container run -it ubuntu bash

# 以detach模式启动容器,并且进入容器交互
docker container run -d -it ubuntu bash

# 先查看container_id，假设这里是9f
docker exec -it 9f bash

# 以detach模式运行
docker run -d 9f /bin/bash
```
## 查看容器日志
```
docker logs CONTAINER_ID

```
## 进入容器
```
docker exec -it CONTAINER_ID /bin/bash
```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。