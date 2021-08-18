---
title: MQTT服务器EMQX的设置登录验证和客户端离在线通知
tags: MQTT,EMQX,Python
renderNumberedHeading: true
grammar_cjkRuby: true
---

[TOC?depth=3]

* [概述](#概述)
* [操作流程](#操作流程)
	* [ 及以前的版本](#及以前的版本)
	* [emqx 4.3 版本](#emqx-43-版本)
		* [修改匿名登录验证设置](#修改匿名登录验证设置)
		* [打开登录校验插件](#打开登录校验插件)
		* [添加用户名和密码](#添加用户名和密码)
		* [修改访问控制配置文件](#修改访问控制配置文件)
* [客户端上线下线的系统消息订阅](#客户端上线下线的系统消息订阅)

# 概述
在使用`python`开发过程中，使用到`MQTT`消息订阅机制以实现业务需求。其中一项便是订阅消息的客户端需要收到关于其他客户端的MQTT服务器`上线与下线`的消息推送。这里记录一下实现的步骤与注意事项。

**操作系统平台与软件版本**：

- 操作系统 ：`Windows 10`
- emqx 版本 ：`emqx 4.3`

**实现的步骤主要有**：

1. 更改客户端订阅验证机制，即`是否允许匿名登录`由允许改为不允许
2. 创建管理员用户名和密码，赋予其系统即消息订阅权限(客户端上下线通知属于系统级消息)
3. 启动用户名密码校验插件功能

**主要的注意事项**：

 - `emqx`的版本区别(`emqx 4.3` 版本和`4.2`以及以前的旧版本的设置方法有区别) 
 - 配置文件修改完成后，需要重启eqmx服务器方可生效

# 操作流程
## `emqx 4.2` 及以前的版本 
`emqx 4.2` 及以前的版本如何更改登录用户名和密码，可通过搜索引擎检索一下，有大量的文档或技术博客有说明，不再赘述。

## emqx 4.3 版本
### 修改匿名登录验证设置
假设 emqx 安装在 `D:\` 盘,[安装教程](https://blog.csdn.net/LJX_ahut/article/details/119189928)，此时，打开系统配置文件，位于`d:\emqx\etc\emqx.conf`,以文本的方式打开，修改配置项`allow_anonymous`为`false`,修改前，系统默认值`true`:
```
## Allow anonymous authentication by default if no auth plugins loaded.
## Notice: Disable the option in production deployment!
##
## Value: true | false
allow_anonymous = false
```
修改完成后，保存退出。

### 打开登录校验插件
登录`127.0.0.1:18083`，输入默认账户名`admin`和默认密码`public`登录控制台，在左侧导航栏点击`Plugins`(中文界面显示的是`插件`)，启动`emqx_auth_mnesia`即可

> 在Emqx4.3版本之前存在一个`emqx_auth_username`扩展，可以通过启动`emqx_auth_username`插件模块修改其配置实现账号密码验证。
>  但在`Emqx 4.3`版本之后不一样了，[官方文档](https://docs.emqx.cn/broker/v4.3/changes/changes-4.3.html#_4-3-0-%E7%89%88%E6%9C%AC) 里有注明`emqx 4.3`版本中`emqx_auth_clientid` 与 `emqx_auth_usernmae` 合并为 `emqx_auth_mnesia`。`emqx_auth_username`模块从此废弃。在`Emqx 4.3`版中加载`emq_auth_username`插件会报不存在的错误,所以不要再去寻找安装`emqx_auth_username`模块了。直接修改`emqx_auth_mnesia.conf`模块配置文件，添加账号密码。



### 添加用户名和密码
找到与插件`emqx_auth_mnesia`对应的配置文件,位于`D:\emqx\etc\plugins\emqx_auth_mnesia.conf`,添加如下用户名和密码：

```
## Password hash.
##
## Value: plain | md5 | sha | sha256 | sha512
auth.mnesia.password_hash = sha256

##--------------------------------------------------------------------
## ClientId Authentication
##--------------------------------------------------------------------

auth.client.1.clientid = admin
auth.client.1.password = your_own_password

##--------------------------------------------------------------------
## Username Authentication
##--------------------------------------------------------------------

## Examples:
auth.user.1.username = admin
auth.user.1.password = your_own_password

```
保存后退出。

### 修改访问控制配置文件
打开`d:\emqx\etc\acl.conf`,添加一行用户访问配置: 

```
{allow, {user, "admin"}, subscribe, ["$SYS/#"]}.
```
允许`admin`用户订阅系统级消息。保存后退出，重启`emqx`服务即可

# 客户端上线下线的系统消息订阅

客户端离线与在线消息属于系统级通知，需要客户端订阅系统预定义的`topic`:



- 离线topic `$SYS/brokers/+/clients/+/disconnected`

- 上线topic `$SYS/brokers/+/clients/+/connected`

- 上下线topic  `$SYS/brokers/+/clients/#`

示例代码：

```
def on_connect(client, userdata, flags, rc):
	# this method will be called when client connected to server successfully
	# TODO do something when this client been notified about successfully connected to server
    pass


def on_message(client, userdata, msg: mqtt.MQTTMessage):
	# this method will be called when this client get a message under the topic(s) it subscribed, encluding the system message （I assuming you've already configure it properly）
	# TODO do something when this client get a message
    pass


mqtt_server = "127.0.0.1"
client = mqtt.Client("surveillance_client")
client.username_pw_set("admin", "aoto@123")
# 定义回调方法
client.on_connect = on_connect
client.on_message = on_message
# 600为keepalive的时间间隔
client.connect(mqtt_server, 1883, 600)
client.subscribe('surveillance', qos=0)
client.subscribe(r"$SYS/brokers/+/clients/#", qos=0)
# 启动mqtt消息订阅(非阻塞式)
client.loop_start()
```

以上代码运行后，若有其他客户端上线或下线，此处`on_message()`回调方法，回收到系统上下线消息，如下所示：

```
客户端上线 topic:  $SYS/brokers/emqx@127.0.0.1/clients/654321/connected
客户端上线消息报文 :
{
  "username": "admin",
  "ts": 1627476021893,
  "sockport": 1883,
  "proto_ver": 4,
  "proto_name": "MQTT",
  "keepalive": 600,
  "ipaddress": "127.0.0.1",
  "expiry_interval": 0,
  "connected_at": 1627476021893,
  "connack": 0,
  "clientid": "654321",
  "clean_start": true
}

客户端下线 topic:  $SYS/brokers/emqx@127.0.0.1/clients/654321/disconnected
客户端下线消息报文 :

{
  "username": "admin",
  "ts": 1627476028659,
  "reason": "tcp_closed",
  "disconnected_at": 1627476028659,
  "clientid": "654321"
}
```
可使用正则表达式`r"^\$SYS\/brokers\/.*\/clients\/.*\/(dis)?connected"`匹配与过滤上下线消息以进行业务逻辑处理。

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。