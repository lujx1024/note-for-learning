[TOC]


# 概述
本文档主要描述`Ubuntu`系统安装完成后，使用普通用户登录后，首次使用`root`用户的设置。包括切换到`root`用户、设置`root`用户密码等


# 系统版本

`Ubuntu 20.04`

# 切换到root用户

## 1. 使用`sudo su`命令

```shell
 sudo su
```

此时系统提示输入当前用户的密码，输入后即可切换到`root`用户。

## 2. 设置`root`用户密码

```shell
 sudo passwd root
```

此时输入需要设置的`root`用户密码，然后再次输入以确认即可.

## 3. 切换到`root`用户

```shell
 su root
```
此时输入`root`用户密码，即可切换到`root`用户。