---
title: CentOS 7 安装 Docker
tags: CentOS,Docker
renderNumberedHeading: true
grammar_cjkRuby: true
---

# 安装前必读
在安装 `Docker `之前，先说一下配置，我这里是 `Centos 7 64位`
 `Linux `内核：官方建议 3.10 以上，3.8以上貌似也可。

> 注意：本文的命令使用的是 `root `用户登录执行，不是 root 的话所有命令前面要加 `sudo`

## 查看系统版本内核
```
uname -r

# 输出
3.10.0-1160.59.1.el7.x86_64
```

## 使用root权限更新yum

> 请注意 ：生产环境中此步操作需慎重，需视情况而定，个人学习请随意
> 这个命令不是必须执行的，后面出现不兼容的情况的话就必须update了
```
yum -y update


相关指令:
yum -y update：升级所有包同时也升级软件和系统内核；​ 
yum -y upgrade：只升级所有包，不升级软件和系统内核
```

## 删除旧版本Docker
> 注 : 此前从未安装过docker组件可跳过此步骤

```
yum remove docker  docker-common docker-selinux docker-engine
```

# Docker 安装

## 安装依赖

yum-util 提供yum-config-manager功能，另两个是devicemapper驱动依赖
```
yum install -y yum-utils device-mapper-persistent-data lvm2
```
## 设置yum源
```
# 中央仓库
yum-config-manager --add-repo http://download.docker.com/linux/centos/docker-ce.repo

# 阿里仓库
yum-config-manager --add-repo http://mirrors.aliyun.com/docker-ce/linux/centos/docker-ce.repo
```

## 选择docker版本并安装
1. 查看现有docker版本

```
yum list docker-ce --showduplicates | sort -r

# 输出
* updates: mirrors.cn99.com
Loading mirror speeds from cached hostfile
Loaded plugins: fastestmirror, langpacks
 * extras: mirrors.ustc.edu.cn
docker-ce.x86_64            3:20.10.9-3.el7                     docker-ce-stable
docker-ce.x86_64            3:20.10.8-3.el7                     docker-ce-stable
docker-ce.x86_64            3:20.10.7-3.el7                     docker-ce-stable
docker-ce.x86_64            3:20.10.15-3.el7                    docker-ce-stable
docker-ce.x86_64            3:20.10.14-3.el7                    docker-ce-stable
docker-ce.x86_64            3:20.10.1-3.el7                     docker-ce-stable
docker-ce.x86_64            3:20.10.13-3.el7                    docker-ce-stable
docker-ce.x86_64            3:20.10.12-3.el7                    docker-ce-stable
docker-ce.x86_64            3:20.10.11-3.el7                    docker-ce-stable
docker-ce.x86_64            3:20.10.10-3.el7                    docker-ce-stable
docker-ce.x86_64            3:20.10.0-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.9-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.8-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.7-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.6-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.5-3.el7                     docker-ce-stable
docker-ce.x86_64            3:19.03.4-3.el7                     docker-ce-stable

```

2. 选择安装版本

> 注 : 不指定版本默认安装最新版本
```
yum -y install docker-ce-19.03.8 docker-ce-cli-19.03.8

# 显示如下所示即表示安装成功
Installed:
  docker-ce.x86_64 3:19.03.8-3.el7                                                       
Dependency Installed:
  container-selinux.noarch 2:2.119.2-1.911c772.el7_8     containerd.io.x86_64 0:1.6.4-3.1.el7
  docker-ce-cli.x86_64 1:20.10.15-3.el7              docker-scan-plugin.x86_64 0:0.17.0-3.el7     
Complete!

```

## 启动docker并设置开机自启
```
systemctl start docker
systemctl enable docker
```

# 使用官方脚本安装
Docker官方提供了一种非常方便的Linux平台安装方式,访问`get.docker.com`地址并保存安装脚本，在本地执行这个脚本即可。
```
# 下载脚本,重命名为docker-install.sh
curl -fsSL https://get.docker.com/ -o docker-install.sh

# 运行脚本,安装最新版docker(非root用户需在指令前加sudo)
sh docker-install.sh
```


欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。
