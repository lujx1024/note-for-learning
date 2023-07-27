[TOC]

# 概述

本文档主要记录Ubuntu系统安装完成后，设置ssh远程访问的过程。

# 系统版本

`Ubuntu 20.04`

# 安装ssh服务

## 1. 安装ssh服务

```shell
 sudo apt-get install openssh-server
```

## 2. 启动ssh服务

```shell
 sudo service ssh start
```

## 3. 查看ssh服务状态

```shell
 sudo service ssh status
```

# 设置ssh远程访问

## 1. 查看ssh服务监听端口

```shell
 netstat -anp | grep ssh
```

## 2. 修改ssh配置文件

```shell
 sudo vim /etc/ssh/sshd_config
```

## 3. 修改配置文件内容

```shell
 # 添加 Port 2222 访问端口，可同时使用多个端口
 Port 22
 Port 2222
 # 将PermitRootLogin prohibit-password修改为PermitRootLogin yes
 PermitRootLogin yes
```

## 4. 重启ssh服务

```shell
 sudo service ssh restart
```

# 设置防火墙

## 1. 查看防火墙状态

```shell
 sudo ufw status
```

## 2. 开启防火墙

```shell
 sudo ufw enable
```

## 3. 查看防火墙状态

```shell
 sudo ufw status
```

## 4. 开启ssh端口

```shell
 sudo ufw allow 22
```

## 5. 开启其他端口

```shell
 sudo ufw allow 2222
```

## 6. 查看防火墙规则

```shell
 sudo ufw status numbered
```

## 7. 删除防火墙规则

```shell
 sudo ufw delete 1
```

## 8. 关闭防火墙

```shell
 sudo ufw disable
```

# 设置ssh免密登录

## 1. 生成密钥

```shell
 ssh-keygen -t rsa 
```

## 2. 查看密钥

```shell
 cd ~/.ssh
 ls
```

## 3. 将公钥复制到远程服务器

```shell
# linux
 ssh-copy-id -i ~/.ssh/id_rsa.pub root@ip

# windows
scp ~/.ssh/id_rsa.pub root@ip:/root/.ssh/authorized_keys
```

## 4. 登录远程服务器

```shell
 ssh root@
```

