---
title: nvidia-docker启动异常Permission denied解决方法
tags: Nvidia-docker,Linux,Permission Denied
renderNumberedHeading: true
grammar_cjkRuby: true
---
# 概述
安装nvidia-docker组件后启动报错`Permission Denied`,导致错误的原因是`SeLinux`功能模块未关闭，将其关闭即可。

> `nvidia-docker`是`docker`的一层封装，`docker`在`root`账号下，应用程序安装在`/usr/bin/docker` 下，`linux`系统自带的`selinux`安全访问控制模块，为保护系统安全，严格控制调用系统程序的权限，即使在`root`账号下，也不允许一个系统程序调用另一个系统程序。因此，调用`nvidia-docker run/images` 等指令，会调用`docker`指令，系统提示权限受限拒绝

# 解决方法

## 临时关闭SELINUX
执行指令 : `setenforce 0`可**临时关闭**SELINUX功能，但是系统重启后恢复

查询当前SELINUX状态:
```
[root@localhost ~]# getenforce
Disabled
```

## 永久关闭SELINUX

编辑文件`/etc/selinux/config`

```
vim /etc/selinux/config
```
设置`SELINUX=disabled`

```   
  # This file controls the state of SELinux on the system.
  # SELINUX= can take one of these three values:
  #     enforcing - SELinux security policy is enforced.
  #     permissive - SELinux prints warnings instead of enforcing.
  #     disabled - No SELinux policy is loaded.
 SELINUX=disabled
 # SELINUXTYPE= can take one of three two values:
 #     targeted - Targeted processes are protected,
 #     minimum - Modification of targeted policy. Only selected processes are protected. 
 #     mls - Multi Level Security protection.
 SELINUXTYPE=targeted
```
执行`reboot`重启机器，完成。
欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。