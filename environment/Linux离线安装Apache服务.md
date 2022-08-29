---
title: Linux离线安装Apache HTTP服务
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---
# 概述
`Apache HTTP`服务支持通过系统包管理器,如`apt-get`或`yum`等在线安装，这里记录一下在机器不支持使用包管理器在线安装时，通过安装包或源码编译的方式安装的方法。
由于`Apache 2.4` 以后的版本不再自带 `APR `库，所以在安装`Apache`之前，需要先安装以下依赖工具：
1. `apr`
2. `apr-util`
3. `pcre`

# 安装流程

## 安装包下载
1. 下载`apr`和`apr-util`
	官方下载页面[链接](https://apr.apache.org/download.cgi)
	`apr-1.7.0`[下载链接](https://dlcdn.apache.org//apr/apr-1.7.0.tar.gz)
	`apr-util-1.6.1`[下载链接](https://dlcdn.apache.org//apr/apr-util-1.6.1.tar.gz)
2. 下载pcre
	`pcre2-10.40`[下载链接](https://github.com/PCRE2Project/pcre2/releases/download/pcre2-10.40/pcre2-10.40.tar.gz)

3. 下载apache http安装包
    官方下载页面[链接](https://httpd.apache.org/download.cgi#apache24)
	`apache httpd-2.4.54`[下载链接](https://dlcdn.apache.org/httpd/httpd-2.4.54.tar.gz)

> 注：以上下载的安装版本为本博文记录时实际安装操作使用的版本，有最新更新或使用其他版本请注意下载链接的有效性

> 注：由于目标安装设备无法联网，以上下载操作均在其他可联网设备进行，下载完成后可使用诸如`scp`指令或`ftp`的方式传入`目标linux主机`

## 编译安装
1. 解压文件
	进入上述压缩文件保存位置时，依次解压文件到指定位置
	```
	cd /home/software_pkgs
	tar -xzvf apr-1.7.0.tar.gz -C /usr/local
	tar -xzvf apr-util-1.6.1.tar.gz -C /usr/local
	tar -xzvf pcre2-10.40.tar.gz -C /usr/local
	tar -xzvf httpd-2.4.51.tar.bz -C /usr/local
	```
2. 安装`apr`
	```
	cd /usr/local/apr-1.7.0
	./configure --prefix=/usr/local/apr
	make
	make install
	```
3. 安装`apr-util`
   ```
   cd /usr/local/apr-util-1.6.1
	./configure --prefix=/usr/local/apr-util --with-apr=/usr/local/apr
	make
	make install
   ```
 4. 安装`pcre`
	```
	cd /usr/local/pcre2-10.40
	./configure --enable-utf8  
	make && make install
	```
5. 安装`apache httpd`

	```
	cd /usr/local/httpd-2.4.48
	./configure --with-apr=/usr/local/apr --with-apr-util=/usr/local/apr-util
	make
	make install
	```
	>注：`httpd`服务默认安装位置是`/usr/local/apache2`

# httpd服务的启动与设置
## 服务的启动与终止
1. apache httpd服务启动 : `/usr/local/apache2/bin/apachectl start`
2. apache httpd服务终止 : `/usr/local/apache2/bin/apachectl stop` 
3. apache httpd服务重启 :  `/usr/local/apache2/bin/apachectl restart`
4. 查看apache运行状态  :  `ps -ef | grep httpd`, 出现`/usr/local/apache2/bin/httpd -k start`的结果，表示运行成功。

## 访问服务
`http server`默认开放端口为`80`，访问`机器IP`地址网页显示`It Works`表示服务已经成功启动

## 配置访问端口
打开配置文件`/usr/local/apache2/conf/httpd.conf`,修改约**52行**配置的监听端口号，例如修改为`8080`
```
#
# Listen: Allows you to bind Apache to specific IP addresses and/or
# ports, instead of the default. See also the <VirtualHost>
# directive.
#
# Change this to Listen on specific IP addresses as shown below to
# prevent Apache from glomming onto all bound IP addresses.
#
#Listen 12.34.56.78:80
# Listen 80
Listen 8088
```

## 配置主页位置
`http server`默认文件保存位置为`/usr/local/apache2/htdocs`，访问`机器IP`地址网页显示`It Works`实质上就是加载该路径下的`index.html`文件.

修改文件`/usr/local/apache2/conf/httpd.conf`约219行和220行，可更换为本地其他路径，
```
# 旧地址
# DocumentRoot "/usr/local/apache2/htdocs"
# 新地址
DocumentRoot "/home/python/projects/paddlegan"
# 旧地址
# <Directory "/usr/local/apache2/htdocs">
# 新地址
<Directory "/home/python/projects/paddlegan">
```


欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。