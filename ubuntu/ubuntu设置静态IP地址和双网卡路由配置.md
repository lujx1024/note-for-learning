[TOC]

# 概述

本文档主要记录`ubuntu`系统设置网卡静态地址与双网卡路由的配置方法。

# 系统版本

`Ubuntu 20.04`

# 设置静态IP地址

## 1. 查看网卡名称

```shell
ifconfig -a
```

## 2. 修改网卡配置文件

```shell
sudo vim /etc/netplan/00-installer-config.yaml
```

> 说明：`00-installer-config.yaml`文件名可能不同，根据实际情况修改。

## 3. 修改配置文件内容

```shell
# This is the network config written by 'subiquity'
network:
  version: 2
  renderer:  NetworkManager
  ethernets:
  	enp0s3: # 网卡名称
  		dhcp4: yes
    enp0s8: # 网卡名称
      dhcp4: no
      addresses: [192.168.1.101/24] # 静态IP地址
        gateway4: 192.168.1.1
        nameservers:
          addresses: [192.168.1.1] # 网关地址
```

> 说明：`enp0s3`和`enp0s8`为网卡名称，根据实际情况修改。


## 4. 使配置文件生效

```shell
sudo netplan apply
```

# 设置双网卡路由

## 1.查看路由表

```shell
route -n
```

## 2.添加路由

```shell
sudo route add -net 0.0.0.0 netmask 0.0.0.0 gw 192.168.1.1 dev enp0s3
```
> 说明：上述指令为添加默认路由，指向互联网,网关地址是`192.168.1.1`,所有的数据包都通过`enp0s3`网卡发送出去。

## 3.删除路由

```shell
sudo route del -net 0.0.0.0 dev enp0s3
```
> 说明：上述指令为删除指向互联网的默认路由。将所有数据包都通过`enp0s3`网卡的路由删除。
