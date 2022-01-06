---
title: CentOS7升级cmake版本
tags: CentOS,CMake,版本升级
renderNumberedHeading: true
grammar_cjkRuby: true
---
# yum安装
`[root@localhost ~]# yum install -y cmake`
# 查看当前系统cmake版本
```
[root@localhost ~]# cmake -version
cmake version 2.8.12.2
```
使用yum安装的cmake有时会因为版本过低导致编译其他软件的源码失败，此时需要将CMake版本升级，本文档记录CMake版本从2.8升级至3.14的操作过程
# 升级流程
## 安装依赖
```
[root@localhost ~]# yum install -y gcc gcc-c++
[root@localhost ~]# mkdir /opt/cmake
[root@localhost ~]# cd /opt/cmake/
```
## 下载3.14版本源码
`[root@localhost cmake]# wget https://cmake.org/files/v3.14/cmake-3.14.5.tar.gz`
## 解压
`[root@localhost cmake]# tar zxvf cmake-3.14.5.tar.gz`

## 删除已安装的cmake
`[root@localhost cmake]# yum remove cmake -y`

## 配置安装环境
`[root@localhost cmake]# ./configure --prefix=/usr/local/cmake`

## 编译并安装
`[root@localhost cmake-3.14.5]# make && make install`

## 创建软连接
`[root@localhost ~]# ln -s /usr/local/cmake/bin/cmake /usr/bin/cmake`

## 修改配置文件
```
[root@localhost ~]# vim /etc/profile
export CMAKE_HOME=/usr/local/cmake
export PATH=$PATH:$CMAKE_HOME/bin
```
## 刷新配置文件
`[root@localhost ~]# source /etc/profile`

## 查看版本
`[root@localhost ~]# cmake -version`

安装完成
欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。