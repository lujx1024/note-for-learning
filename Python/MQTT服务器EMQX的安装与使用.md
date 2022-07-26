---
title: MQTT服务器EMQX的安装与使用
tags: Windows,MQTT,安装
renderNumberedHeading: true
grammar_cjkRuby: true
---
[TOC]

# 说明

MQTT服务器选择 EMQX ，[下载链接](https://www.emqx.cn/downloads#broker)

安装包支持包括`MacOS`、`Windows`、`Linux`各发行版以及`Docker`方式安装，在安装前选择对应平台的版本，这里主要记录`Windows`平台和`Linux`发行版`CentOS`平台的环境安装，以及使用`python`语言进行消息订阅与推送的示例代码。

# Windows平台安装

进入下载页面，选择`windows`图标<i class="fab fa-windows fa-border"></i>，本示例下载的文件及版本为：`emqx-windows-4.3.5.zip` 

解压上述文件至D盘(本实例使用的是D盘，可选择其他盘)，进入命令行，切换目录至 d:\emqx\bin

```
# 进入安装盘
C:\Users\lujx>d:
# 进入安装bin目录
D:\>cd emqx\bin
# 安装服务
D:\emqx\bin>emqx install
# 输出：
D:\emqx\erts-11.0\bin\erlsrv.exe: Service emqx_4.3.5 added to system.
[SC] ChangeServiceConfig 成功
# 启动服务
D:\emqx\bin>emqx start
```
# CentOS平台安装
同上，进入下载页面，鼠标点击`CentOS`图标<i class="fab fa-centos fa-border"></i>，选择与安装平台对应的操作系统的版本号以及安装包的打包方式，本实例使用的是`CentOS 7` 64位的`amd`芯片结构的`zip`安装`emqx-centos7-4.3.5-amd64.zip`，[下载链接](https://github.com/emqx/emqx/releases/download/v4.3.5/emqx-centos7-4.3.5-amd64.zip)

```
# 解压文件到安装目录，本示例使用的是/usr/local/,此目录可自行指定
unzip emqx-centos7-4.3.5-amd64.zip -d /usr/local/
# 进入目录
cd /usr/local/emqx
# 启动服务
./bin/emqx start
```
# 控制台访问

启动后即可访问`http://localhost:18083 `进入登入页面
默认用户名：`admin`，密码：`public`

# Python语言实现消息收发

python语言提供了mqtt依赖库paho-matt，用来提供与mqtt服务器进行数据交互的接口.
首先安装依赖包：
`pip install paho-mqtt`

## 消息推送
```
import datetime
import time

import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

mqtt_server = "127.0.0.1"
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_server, 1883, 600)  # 600为keepalive的时间间隔

while True:
    msg = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
    # 消息推送 
    client.publish('test', payload=msg, qos=0)
    time.sleep(0.02)
```

## 消息订阅

```
def on_connect(client: mqtt.Client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg: mqtt.MQTTMessage):
    global msg_global
    msg_global = str(msg.payload, encoding='utf-8')

mqtt_server="127.0.0.1"
client = mqtt.Client()
# 设置连接成功事件回调函数
client.on_connect = on_connect
# 设置收到消息后的回调函数
client.on_message = on_message
client.connect(mqtt_server, 1883, 600)  # 600为keepalive的时间间隔
client.subscribe('test', qos=0)
client.loop_forever()  # 保持连接 阻塞式
```

## 阻塞式与非阻塞式消息订阅
在上述示例中，使用`client.loop_forever()`的方式开启消息订阅，此方法是阻塞式的，也就是说，任何写在此行代码之后的代码将不被执行。

同样，paho-mqtt提供了非阻塞式方法`client.start_loop()`,在其后可使用循环处理业务逻辑，贴一下示例代码，如下：
```
import datetime
import time

import paho.mqtt.client as mqtt

msg_global = ""

def on_connect(client: mqtt.Client, userdata, flags, rc):
    print("Connected with result code: " + str(rc))

def on_message(client, userdata, msg: mqtt.MQTTMessage):
    global msg_global
    msg_global = str(msg.payload, encoding='utf-8')

mqtt_server="127.0.0.1"
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(mqtt_server, 1883, 600)  # 600为keepalive的时间间隔
client.subscribe('test', qos=0)
# client.loop_forever()  # 保持连接 阻塞式
client.loop_start()  # 启动连接 非阻塞式

# 业务处理，回调方法中，将收到的消息用过全局变量接收，在主线程中使用此全局变量。
while True:
    if msg_global is not None:
        local_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S:%f')
        print(local_time, msg_global)
        msg_global = None
```


欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。