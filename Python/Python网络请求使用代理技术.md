---
title: Python网络请求使用代理技术
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---

## 代理软件

在本机安装并运行相关代理软件，这种方式获取的代理IP与启动代理软件时的配置有关——例如，使用`V2ray`代理软件时它会在本地 `10809`端口上创建 HTTP 代理服务，也就是说代理IP为 `127.0.0.1:10809`，另外还会在 `10808` 端口创建 `SOCKS 5`代理服务，也就是代理IP为 `127.0.0.1:10808`。同样，在下一部分各个请求库的代理设置中使用这些代理IP（`127.0.0.1:10808`，`127.0.0.1:10809`）即可，而爬虫所带的伪装IP则是代理软件V2ray所连接的服务器 IP.


## Requests使用代理

### HTTP代理

对于 `Requests `来说，代理设置比较简单，我们只需要传入` proxies` 参数即可。在这里，我们使用本机代理软件创建的`HTTP `代理服务，进行`Requests` 的代理的设置，如下：

```
import requests

proxy = '127.0.0.1:10809'
proxies = {
	'http': 'http://' + proxy,
	'https': 'https://' + proxy,
}
try:
	response = requests.get('http://httpbin.org/get', proxies=proxies)
	print(response.text)
except requests.exceptions.ConnectionError as e:
	print('Error', e.args)
```

如果代理需要认证，同样在代理的前面加上用户名密码即可，代理的写法就变成：
```
proxy = 'username:password@127.0.0.1:10809'
```

### SOCKS 代理

首先安装`python`依赖库`requests[socks]`

```
pip install "requests[socks]"
```
设置代理代码如下：
```
import requests
 
proxy = '127.0.0.1:10808'
proxies = {
    'http': 'socks5://' + proxy,
    'https': 'socks5://' + proxy
}
try:
    response = requests.get('http://httpbin.org/get', proxies=proxies)
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)
```

还有一种使用 `socks `模块进行全局设置的方法，如下：
```
import requests
import socks
import socket
 
socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 10808)
socket.socket = socks.socksocket
try:
    response = requests.get('http://httpbin.org/get')
    print(response.text)
except requests.exceptions.ConnectionError as e:
    print('Error', e.args)
```

## Selenium 使用代理

`Selenium `也可以设置代理，在设置方法上分有无界面的浏览器两种方法，因此对于有界面浏览器，将以 `Chrome `为例介绍；而对于无界面浏览器，以 `PhantomJS `为例介绍。

### Chrome浏览器

对于 `Chrome `来说，用 `Selenium `设置代理的方法也非常简单，设置方法如下：

```
from selenium import webdriver
 
proxy = '127.0.0.1:10809'
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server=http://' + proxy)
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('http://httpbin.org/get')
```

### PhantomJS

对于 `PhantomJS`，代理设置方法可以借助于 `service_args `参数，也就是命令行参数；在这里我们只需要使用 `service_args `参数，将命令行的一些参数定义为列表，在初始化的时候传递即可。

因此，代理设置方法如下：
```
from selenium import webdriver
 
service_args = [
    '--proxy=127.0.0.1:10809',
    '--proxy-type=http'
]
browser = webdriver.PhantomJS(service_args=service_args)
browser.get('http://httpbin.org/get')
print(browser.page_source)
```
如果需要认证，那么只需要再加入` –proxy-auth` 选项即可，这样参数就改为：
```
service_args = [
    '--proxy=127.0.0.1:10809',
    '--proxy-type=http',
    '--proxy-auth=username:password'
]
```
将 `username `和 `password `替换为认证所需的用户名和密码即可

参考资料：
- https://blog.csdn.net/yangzhou9177/article/details/104891959

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。