---
title: Program With Mosh -- Docker Windows平台的安装与第一次启动
tags: Docker
category: Mosh/Docker笔记
renderNumberedHeading: true
grammar_cjkRuby: true
---

# Get start

## windows 10安装Docker

### 安装包下载

登录docker官方网站，[链接地址](https://www.docker.com/products/docker-desktop) 下载指定平台的安装包即可。
本文档在编写时，操作系统是windows 10。因此，下面记录的是在windows平台上的操作流程

### 启用 Hyper-V功能

Win10系统安装Docker前，需要启用Hyper-V windows功能。点击win徽标进入设置，搜索"启用或关闭windows功能"，将Hyper-V勾选即可。启用后需要重启。

### 安装docker
直接双击exe安装文件即可。安装完成后，可修改images保存地址，由于默认保存在c盘，会占用有限的空间，可修改地址到其他路径。右击任务栏鲸鱼docker图标鲸鱼![](./images/1617385881277.png)-->settings-->Resource-->Advanced-->Disk image location,选择一个新路径后，点击 Apply 即可。

### docker 第一次运行指令

#### 基础运行指令
 - docker version   ## 查看当前安装的docker版本
 - docker info  ## 查看当前的docker配置信息
 - docker run ubuntu
 #### 指令解释
 
-   `docker run ubutun`
     使用docker容器运行本地的ubuntu镜像，如本地没有ubuntu镜像，则直接从远程hub下载。
     指令实行完成后，输出信息如下：
	 ```
	 C:\Users\John
	λ docker run ubuntu
	Unable to find image 'ubuntu:latest' locally
	latest: Pulling from library/ubuntu
	04a5f4cda3ee: Pull complete
	ff496a88c8ed: Pull complete
	0ce83f459fe7: Pull complete
	Digest: sha256:a15789d24a386e7487a407274b80095c329f89b1f830e8ac6a9323aa61803964
	Status: Downloaded newer image for ubuntu:latest
	 ```
  - `docker ps -a   ## 查询当前docker中的所有容器` 
  - `docker run -it ubutun   ## docker 启动这个ubuntu镜像,参数 i 表示interact交互；t 表示terminal终端` 
  -  启动镜像后，终端显示如下
	  ```
		λ docker run -it ubuntu
		root@af187c080d37:/#
		
		root:docker镜像ubuntu操作系统的当前登录用户
		af187c080d37: container编号
		```
  
欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。