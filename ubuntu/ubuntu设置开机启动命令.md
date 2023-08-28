[TOC]

# 概述

本文档主要记录`Ubuntu`系统使用`/etc/rc.local`设置开机指令的方法。

# 系统版本

`Ubuntu 20.04`

# 设置开机启动命令

## 1. 查看`rc-local`服务状态

```shell
sudo systemctl status rc-local
```

输出结果如下:

```text
root@localhost:~$ systemctl status rc-local
● rc-local.service - /etc/rc.local Compatibility
     Loaded: loaded (/lib/systemd/system/rc-local.service; static; vendor preset: enabled)
    Drop-In: /usr/lib/systemd/system/rc-local.service.d
             └─debian.conf
     Active: inactive (dead)
       Docs: man:systemd-rc-local-generator(8)
```

## 2. 设置`rc-local`服务开机启动

```shell
sudo systemctl enable rc-local
```

> 注: Ubuntu 20.04不能直接启用`rc-local`服务，会报错，需要手动创建`rc-local`服务文件。指令报错如下:

```text
root@localhost:~$ sudo systemctl enable rc-local
[sudo] password for simple:
The unit files have no installation config (WantedBy=, RequiredBy=, Also=,
Alias= settings in the [Install] section, and DefaultInstance= for template
units). This means they are not meant to be enabled using systemctl.

Possible reasons for having this kind of units are:
• A unit may be statically enabled by being symlinked from another unit's
  .wants/ or .requires/ directory.
• A unit's purpose may be to act as a helper for some other unit which has
  a requirement dependency on it.
• A unit may be started when needed via activation (socket, path, timer,
  D-Bus, udev, scripted systemctl call, ...).
• In case of template units, the unit is meant to be enabled with some
  instance name specified.
```

## 3. 手动创建系统自启动服务

```shell
sudo vim /etc/systemd/system/rc-local.service
```

输入以下内容:

```text
[Unit]
 Description=/etc/rc.local Compatibility
 ConditionPathExists=/etc/rc.local
[Service]
 Type=forking
 ExecStart=/etc/rc.local start
 TimeoutSec=0
 StandardOutput=tty
 RemainAfterExit=yes
 SysVStartPriority=99
[Install]
 WantedBy=multi-user.target
 ```

## 4. 创建`rc.local`文件

```shell
sudo vim /etc/rc.local
```

输入以下内容:

```text
#!/bin/sh -e
#
# rc.local
#
# This script is executed at the end of each multiuser runlevel.
# Make sure that the script will "exit 0" on success or any other
# value on error.
#
# In order to enable or disable this script just change the execution
# bits.
#
# By default this script does nothing.
# Print the IP address
# _IP=$(hostname -I) || true
# if [ "$_IP" ]; then
#   printf "My IP address is %s\n" "$_IP"
# fi
exit 0
```

## 5. 设置`rc.local`文件权限

```shell
sudo chmod +x /etc/rc.local
```

## 6.添加开机启动命令

以删除某条冗余静态路由为例，例如，现在有双网卡环境，需要将其中一张网卡用于内网数据传输，另外一张网卡用于访问互联网数据传输,但是在配置完成后，发现内网数据传输正常，但是互联网数据传输异常，经过排查发现，是因为在配置内网网卡时，误将内网网卡的默认网关设置为了内网网关，导致互联网数据传输异常，因此需要删除该条冗余静态路由。删除指令为`sudo route del -net 0.0.0.0 dev enp0s8`,现在希望在开机时自动执行该指令，因此需要将该指令添加到`rc.local`文件中。

```shell
sudo vim /etc/rc.local
```

在`exit 0`前添加以下内容:

```text
sudo route del -net 0.0.0.0 dev enp0s8
```

## 7.启用`rc-local`服务

```shell
sudo systemctl start rc-local
sudo systemctl enable rc-local
```

## 8.查看`rc-local`服务状态

```shell
sudo systemctl status rc-local
```

## 9.重启系统

```shell
sudo reboot
```

系统完成重启后，可查看路由表，发现冗余静态路由已被删除。

