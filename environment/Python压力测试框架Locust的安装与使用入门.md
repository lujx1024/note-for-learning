---
title: Python压力测试框架Locust的安装与使用入门
tags: 压力测试,Locust,Python
renderNumberedHeading: true
grammar_cjkRuby: true
---
# 概述

`Locust`是一个易于使用、可编写脚本和可扩展的性能测试工具。您可以用常规的`Python`代码定义用户的行为，而不是被困在UI或限制性的领域特定语言中。这使得`Locust`具有无限的可扩展性，并且对开发人员非常友好。


`Locust`的诞生源于对现有解决方案的失望。没有任何现有的负载测试工具能够很好地针对动态网站生成真实的负载，因为大多数页面针对不同的用户具有不同的内容。现有的工具使用笨拙的接口或冗长的配置文件来声明测试。在`Locust`中，我们采取了不同的方法。而不是配置格式或`ui`，你会得到一个python框架，让你使用`python`代码定义用户的行为。

`Locust`直译为蝗虫,得名于一种蚱蜢，以其群集行为而闻名。

以前版本的`Locust`使用了从自然中借来的术语(`群集`，`孵化`，`攻击`等)，但现在使用了更多的行业标准命名。

# 安装

> 执行安装步骤前需安装`python`解释器环境

1. 安装
	`pip install locust`
2. 校验
   `locust -V`
3. 升级
   `pip3 install -U --pre locust`
   
   
  # 使用
  ## 最简单的使用
   ```
	from locust import HttpUser, task

	class HelloWorldUser(HttpUser):
		@task
		def hello_world(self):
			self.client.get("/hello")
			self.client.get("/world")
   ```
   启动
   `locust -f thisfile.py`
   
 ## 编写测试脚本
 
 ```
import time
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)
	host = 'http://127.0.0.1:8000'

    @task
    def hello_world(self):
        self.client.get("/hello")
        self.client.get("/world")

    @task(3)
    def view_items(self):
        for item_id in range(10):
            self.client.get(f"/item?id={item_id}", name="/item")
            time.sleep(1)

    def on_start(self):
        self.client.post("/login", json={"username":"foo", "password":"bar"})

 ```
 
 ## 脚本解析
 ```
 import time
 from locust import HttpUser, task, between
 ```
 locust是python模块，使用时直接导入即可
 
 ```
 class QuickstartUser(HttpUser):
 ```
这里定义一个类，用来模拟用户,继承自 `HttpUser` 包含一个`client`成员, 该成员是'`HttpSession`的实例对象，可以向测试的系统发送http请求
```
wait_time = between(1, 5)
```

设置执行任务的间隔时间，随机选取1到5秒 
```
@task
def hello_world(self):
    ...
```

使用装饰器`@task`定义任务方法

```
@task
def hello_world(self):
    self.client.get("/hello")

@task(3)
def view_items(self):
...
```
这里定义了两个任务，其中一个任务给了更高的权重3,程序运行过程中，会随机挑选已定义的任务进行执行，权重越高，该任务被选中的执行几率就越高，选中的任务执行完成后，会进行休眠1-5秒(上面的设置)，然后在进行随机任务的挑选执行，如此重复
```
self.client.get("/hello")
```
使用类定义中的`client`成员发起`request`请求，请求模式等同于`requests`模块
 
 
 
 
 
 
 
 
欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。