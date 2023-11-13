[TOC]

# 概述

在使用`ubuntu`系统的时候，有时候会出现`Temporary failure in name resolution`的问题，这个问题的原因是DNS解析出现了问题，解决这个问题的方法有很多，这里介绍一种比较简单的方法。

报错`Temporary failure in name resolution error`是系统的网络连接问题.会导致无法安装包、收发邮件或发起网络请求。

这个错误会在用户尝试与网站通信、更新系统或执行任何需要活动互联网连接的操作时出现。

例如，当使用ping等命令时，就会出现这个问题：

```bash
ping baidu.com
```

系统无法与DNS服务器通信并返回错误：

```text
[root@localhost ~]# ping baidu.com
ping: baidu.com: Temporary failure in name resolution
[root@localhost ~]#
```

# 解决方法

> 注: 在修改配置文件之前，需要先检查硬件的网络连接是否正常，包括但不仅限于网卡接口、网线、路由器、交换机等是否能正常工作。

The resolv.conf file is a file for configuring DNS servers on Linux systems. Follow the steps below to ensure the file is configured correctly.

Linux系统的resolv.conf文件是用于配置DNS服务器的文件。按照以下步骤确保文件正确配置：

1. 打开`resolv.conf`文件，使用`vim`等文本编辑器打开:

    ``` bash
    vim /etc/resolv.conf
    ```

2. 确保`resolv.conf`文件至少包含一个`nameserver`。列出`nameserver`的行应该像这样：

    ```bash
    nameserver 8.8.8.8
    nameserver 192.168.8.1
    ```

    > 注: 如果没有`nameserver`行，或者没有任何行，就需要添加`nameserver`行。
    > 注：如果不知道添加哪一个，就将当前的路由器网关地址添加进去。

3. 保存文件并退出。
4. 接下来，重启DNS解析器服务。运行以下命令：

```bash
sudo systemctl restart systemd-resolved
```

若指令执行成功，则不会有任何错误信息输出。

5. 最后，再次尝试ping命令，看是否能够正常工作。

```text
[root@localhost ~]# ping baidu.com
PING baidu.com (39.156.66.10) 56(84) bytes of data.
64 bytes from 39.156.66.10 (39.156.66.10): icmp_seq=1 ttl=50 time=28.5 ms
64 bytes from 39.156.66.10 (39.156.66.10): icmp_seq=2 ttl=50 time=28.3 ms
64 bytes from 39.156.66.10 (39.156.66.10): icmp_seq=3 ttl=50 time=28.6 ms
^C
--- baidu.com ping statistics ---
3 packets transmitted, 3 received, 0% packet loss, time 2002ms
rtt min/avg/max/mdev = 28.357/28.524/28.633/0.119 ms
```
