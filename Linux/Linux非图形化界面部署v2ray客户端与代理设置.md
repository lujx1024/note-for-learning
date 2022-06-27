---
title: Linux非图形化界面部署v2ray客户端与代理设置
tags: Linux,v2ray,代理
renderNumberedHeading: true
grammar_cjkRuby: true
---

[TOC]

# 客户端的安装

关于`Linux`平台安装`v2ray`客户端，`GitHub`有提供一键安装的脚本服务，链接地址是 : `https://github.com/v2fly/fhs-install-v2ray`

## 安装步骤

1. 安装`curl`工具`
```
## ubuntu 平台
sudo apt install curl 

## redhat 或 centos
sudo yum install curl
```
2. 执行安装脚本
```
//安装和更新 v2ray
sudo bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh)
//移除 v2ray
sudo bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-release.sh) --remove
//只更新.dat数据
sudo bash <(curl -L https://raw.githubusercontent.com/v2fly/fhs-install-v2ray/master/install-dat-release.sh)
```
## 手动下载安装
由于设置代理之前，`https://raw.githubusercontent.com`这个网站访问不一定顺利，可能会报一下这个错误：
```
curl: (35) OpenSSL SSL_connect: SSL_ERROR_SYSCALL in connection to raw.githubusercontent.com:443
```
所以，也可以把 `install-release.sh`，`install-dat-release.sh` 下载到本地，然后直接本地终端 `bash`执行。

> 执行脚本后，会下载安装包后执行安装，由于网速等原因，可能需要等待一段时间

安装日志如下：
```
info: Installing V2Ray v4.45.2 for x86_64
Downloading V2Ray archive: https://github.com/v2fly/v2ray-core/releases/download/v4.45.2/v2ray-linux-64.zip

Downloading verification file for V2Ray archive: https://github.com/v2fly/v2ray-core/releases/download/v4.45.2/v2ray-linux-64.zip.dgst
info: Extract the V2Ray package to /tmp/tmp.rKuusazxbB and prepare it for installation.
info: Systemd service files have been installed successfully!
~~~~~~~~~~~~~~~~
[Unit]
Description=V2Ray Service
Documentation=https://www.v2fly.org/
After=network.target nss-lookup.target

[Service]
User=nobody
CapabilityBoundingSet=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
AmbientCapabilities=CAP_NET_ADMIN CAP_NET_BIND_SERVICE
NoNewPrivileges=true
ExecStart=/usr/local/bin/v2ray -config /usr/local/etc/v2ray/config.json
Restart=on-failure
RestartPreventExitStatus=23

[Install]
WantedBy=multi-user.target
# In case you have a good reason to do so, duplicate this file in the same directory and make your customizes there.
# Or all changes you made will be lost!  # Refer: https://www.freedesktop.org/software/systemd/man/systemd.unit.html
[Service]
ExecStart=
ExecStart=/usr/local/bin/v2ray -config /usr/local/etc/v2ray/config.json
~~~~~~~~~~~~~~~~

installed: /usr/local/bin/v2ray
installed: /usr/local/bin/v2ctl
installed: /usr/local/share/v2ray/geoip.dat
installed: /usr/local/share/v2ray/geosite.dat
installed: /usr/local/etc/v2ray/config.json
installed: /var/log/v2ray/
installed: /var/log/v2ray/access.log
installed: /var/log/v2ray/error.log
installed: /etc/systemd/system/v2ray.service
installed: /etc/systemd/system/v2ray@.service
removed: /tmp/tmp.rKuusazxbB
info: V2Ray v4.45.2 is installed.
You may need to execute a command to remove dependent software: yum remove curl unzip
Please execute the command: systemctl enable v2ray; systemctl start v2ray

```
安装后，受影响的文件和文件夹：
```
/usr/local/bin/v2ray
/usr/local/bin/v2ctl
/usr/local/share/v2ray/geoip.dat
/usr/local/share/v2ray/geosite.dat
/usr/local/etc/v2ray/config.json
/var/log/v2ray/
/var/log/v2ray/access.log
/var/log/v2ray/error.log
/etc/systemd/system/v2ray.service
/etc/systemd/system/v2ray@.service
```
## 配置文件
默认配置文件位置 :  `/usr/local/etc/v2ray/config.json`，把搭建好的服务配置`config.json`文件里面，保存关闭。

> 建议直接复制图形界面中已配置好的config.json文件直接覆盖，例如windows系统中的配置文件

## 常用指令

1. 启动v2ray服务 : `systemctl start v2ray`
2. 关闭v2ray服务 : `systemctl stop v2ray`
3.  查看v2ray状态 : `systemctl status v2ray`
4. 启动v2ray服务 : `systemctl restart v2ray`
5. 开机启动v2ray服务 : `systemctl enable v2ray`
6. 取消开机启动v2ray服务 : `systemctl disable v2ray.service --now`

> 设置了开机启动服务后，如果有GUI的话，直接打开【系统设置】- 【网络】-【代理】，填写代理地址和端口，点击【应用】，就可以 google 了。

# 代理的设置

## 概述
`代理`是通过`客户端`与`服务端`通信,传输`服务端`能够访问到的资源文件,再由`服务端`通信返回给`客户端`,从而`间接访问`服务端能访问的资源.
以`socket5`通信为例子,我们通过客户端向服务端发送`socket`通信,服务端访问资源再由`socket`通信返回给客户端.但是这里面的通信设置必须通过端口来进行通信,类似`switchyomega`设置过程一样,我们会设定走的代理方式是`127.0.0.1:10808`;这个意思就是通过本地的`10808`端口来进行通信.
以`v2ray客户端`为例，默认是`socket5`通信且端口是`10808`,即`127.0.01:10808`的方式
1.  socks5代理 : `socks5://127.0.0.1:10808`
2. http代理 :  `http://127.0.0.1:10809`

## Linux终端代理设置

### **方法一：（推荐使用）**
这种方法仅仅作用于当前的终端，算是一个临时设置，关闭终端或重启机器后，该设置无效，在终端中直接运行：
`export http_proxy=http://proxyAddress:port`

如果使用http协议的代理，默认端口是10809，想执行wget或者curl来下载国外的东西，可以使用如下命令：
```
export http_proxy=http://127.0.0.1:10809
export https_proxy=http://127.0.0.1:10809
```
使用socket5代理协议的话，默认端口是10808
```
export http_proxy="socks5://127.0.0.1:10808"
export https_proxy="socks5://127.0.0.1:10808"
```

### **方法二 ：(永久设置)**
可直接将代理配置写入shell配置文件`.bashrc`或者`.zshrc`.
直接在`.bashrc`或者`.zshrc`添加下面内容
```
export http_proxy="http://localhost:port"
export https_proxy="http://localhost:port"
```
或者走`socket5`协议的话，代理端口是10808
```
export http_proxy="socks5://127.0.0.1:10808"
export https_proxy="socks5://127.0.0.1:10808"
```
或者干脆直接设置`ALL_PROXY`
```
export ALL_PROXY=socks5://127.0.0.1:10808
```
最后在执行如下命令应用设置 : `source ~/.bashrc`
或者通过设置`alias`简写来简化操作，每次要用的时候输入`setproxy`，不用了就`unsetproxy`.
```
 alias setproxy="export ALL_PROXY=socks5://127.0.0.1:10808" 
 alias unsetproxy="unset ALL_PROXY"
 ```
 
### **方法三 `apt `、`git `设置代理:**
1. `apt `设置
`sudo vim /etc/apt/apt.conf`
	在文件末尾加入下面这行

	`Acquire::http::Proxy "http://proxyAddress:port"`
	
	> 参考链接 : [ubuntu set proxy](https://www.serverlab.ca/tutorials/linux/administration-linux/how-to-set-the-proxy-for-apt-for-ubuntu-18-04/)


2. `git `设置代理
	```
	# 设置代理
	git config --global http.proxy socks5://127.0.0.1:10808
	git config --global https.proxy socks5://127.0.0.1:10808
	# 取消代理设置
	git config --global --unset http.proxy
	git config --global --unset https.proxy
	```
	
3. wget设置代理
	```
	vim ~/.wgetrc

	复制
	#You can set the default proxies for Wget to use for http, https, and ftp.
	# They will override the value in the environment.
	https_proxy = http://127.0.0.1:10809/
	http_proxy = http://127.0.0.1:10809/
	ftp_proxy = http://127.0.0.1:10809/

	# If you do not want to use proxy at all, set this to off.
	use_proxy = on
	```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。