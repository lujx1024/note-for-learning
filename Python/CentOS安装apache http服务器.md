---
title: 2021-04-13 CentOS 安装httpd服务 
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---

### 安装服务
使用`yum`包管理器直接安装即可
`yum install httpd -y`

Apache httpd服务的配置文件位于`/etc/httpd/conf`和`/etc/httpd/config.d`两个文件夹中。网站的数据默认位于`/var/www`,此配置可修改。

### 修改配置文件

主要修改位于`/etc/httpd/conf/httpd.conf`位置的文件。

#### 监听端口
修改配置文件约42行，关于监听端口，本实例使用8088
` Listen 8088`

#### 网站页面默认HTML页面位置

`DocumentRoot`配置项默认指定的是`/var/www/html/`，该配置项可改可不改

#### 防火墙端口设置

1. 查询TCP/UDP的80端口占用情况：
  ```
  firewall-cmd --query-port=8088/tcp
   
  firewall-cmd --query-port=8088/udp
  ```
  
  如果返回 `no`,则表示端口尚未开放，需要开放防火墙端口设置
  
 2. 永久开放 8088 端口
  ```
  firewall-cmd --permanent --zone=public --add-port=8088/tcp
  firewall-cmd --permanent --zone=public --add-port=8088/udp
  ```
  3. 刷新防火墙规则
  ```
  firewall-cmd --reload
  ```
  
  ### 创建index.html文件
  在上文中提到的配置项`DocumentRoot`指定的目录`/var/www/html/`创建简单的HTML文件，简单输入"It works" 即可。
 ```
 cd /var/www/html/
 vim index.html
 # 键入 It works 后保存退出
 
 chown apache.apache index.html
 ```
 
 ### 启动apache服务
 ```
 systemctl start httpd
 
 systemctl status httpd
 
 
[root@localhost ~]# systemctl status httpd
● httpd.service - The Apache HTTP Server
   Loaded: loaded (/usr/lib/systemd/system/httpd.service; disabled; vendor preset: disabled)
   Active: active (running) since Tue 2021-04-13 19:19:53 CST; 36min ago
     Docs: man:httpd(8)
           man:apachectl(8)
  Process: 26009 ExecStop=/bin/kill -WINCH ${MAINPID} (code=exited, status=0/SUCCESS)
 Main PID: 26051 (httpd)
   Status: "Total requests: 4; Current requests/sec: 0; Current traffic:   0 B/sec"
    Tasks: 7
   CGroup: /system.slice/httpd.service
           ├─26051 /usr/sbin/httpd -DFOREGROUND
           ├─26052 /usr/sbin/httpd -DFOREGROUND
           ├─26053 /usr/sbin/httpd -DFOREGROUND
           ├─26054 /usr/sbin/httpd -DFOREGROUND
           ├─26055 /usr/sbin/httpd -DFOREGROUND
           ├─26056 /usr/sbin/httpd -DFOREGROUND
           └─26062 /usr/sbin/httpd -DFOREGROUND

Apr 13 19:19:53 localhost.localdomain systemd[1]: Starting The Apache HTTP Server...
Apr 13 19:19:53 localhost.localdomain httpd[26051]: AH00558: httpd: Could not reliably determine the server's ful...sageApr 13 19:19:53 localhost.localdomain systemd[1]: Started The Apache HTTP Server.
Hint: Some lines were ellipsized, use -l to show in full. 
 
 ```
 
 ### 浏览器访问
 
 使用浏览器，在地址栏中键入`http://your_http_server_ip:8088`,网页显示`It works` 则表示服务部署成功
 
 ### 开启目录结构
 
 #### 修改配置文件welcome.conf
 
 修改配置文件`/etc/httpd/conf.d/welcome.conf`中的`-`号为`+`
 原始配置：`Options -Indexed`
 修改为：`Options +Indexes`
 
 #### 重启服务
 此时可删除此前创建的HTML文件,`/var/www/html/index.html`
 
 执行`systemctl restart httpd`指令即可重启服务
 
 #### 修改默认文件目录
 
 此配置需要修改配置文件`/etc/httpd/conf/httpd.conf`中的三处配置项，本实例中，使用`/home/httpd_files/faceMagician`作为文本保存路径
 
 1. 修改参数`DocumentRoot` 119行
   ```
	默认配置
	# DocumentRoot "/var/www/html"

	修改后的配置
	DocumentRoot "/home/httpd_files/faceMagician"
   
   ```
   2. 修改两个目录参数`Directory` 124行和130 255
   ```
	默认配置
	# <Directory "/var/www">

	修改后的配置
	<Directory "/home/httpd_files">

	默认配置
	# DocumentRoot "/var/www/html"

	修改后的配置
	DocumentRoot "/home/httpd_files/faceMagician"
   ```
   确保指向的文件夹目录存在后，重启服务即可