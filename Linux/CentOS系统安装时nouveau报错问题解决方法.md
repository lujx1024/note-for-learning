---
title: CentOS系统安装时nouveau报错问题解决方法
tags: CentOS,nouveau,解决方案
renderNumberedHeading: true
grammar_cjkRuby: true
---
[toc]

# 概述
这里记录一下在安装CentOS 7 操作系统时遇到的关于nouveau的问题以及解决方案.

nouveau简单来说是一群开源大佬在nvidia的帮助下开发的GPU开源的非官方驱动程序,本次安装操作系统时出现这种情况可能与物理机CPU没有核显有关.
> 注: 物理机配置为i7-7700 无核显CPU + GTX 1050 Ti 显卡,命令行显示正常,GUI无法显示.

在进入启动界面,并选择`Install Centos 7`选项后,显示如下错误:
```
[	6.63524] nouveau 0000:01:00.0 aux 0007 timeout
[	6.63524] nouveau 0000:01:00.0 aux 0007 timeout
[	6.63524] nouveau 0000:01:00.0 aux 0007 timeout
[	6.63524] nouveau 0000:01:00.0 aux 0007 timeout
```
这种情况一般出现在无板载VGA接口且使用显卡作为显示输出的机器

# 解决方法

## 安装阶段
在进入启动界面,不直接选择`Install Centos 7`选项,使用`tab`或`e`键进入编辑模式,此时界面光标显示在如下一行:
```
vmlinuz initrd=initrd.img inst.stage2=hd:LABEL=CentOS\x207\x20x86_64rd.live.check quiet
```
使用退格键,删除`quite`,并添加`nouveau`禁用选项,如下(两项有空格):
```
rdblacklist=nouveau nouveau.modeset=0
```

最终的代码如下:
```
vmlinuz initrd=initrd.img inst.stage2=hd:LABEL=CentOS\x207\x20x86_64rd.live.check rdblacklist=nouveau nouveau.modeset=0

```
使用组合键 `ctrl+x` , 执行安装流程即可顺利进行.

## 首次进入系统阶段
系统安装完成后需要重启并勾选同意协议的选项,再次进入系统同样会遇到`nouveau`的问题,解决方案如下:
1. 在选择内核启动的页面,不使用Enter,使用按键e进入内核编辑模式
2. 移动当前光标至下面一行的代码处
	```
	linux16 /vmlinuz-3.10.0-1160.el7.x86_64 root=/dev/mapper/centos-root ro spectrc-v2=retpoline rd.lvm.lv=centos/root rd.lvm.lv=centos/swap rhgb quite LANG=en_US.UTF-8
	```
3.  删除`quite`,添加`rd.live.check rdblacklist=nouveau nouveau.modeset=0`,每一项中间加空格
4.  使用组合键 `ctrl+x` 进入操作系统.

## 操作系统使用阶段

上述使用内核编辑模式禁用nouveau的手段是临时性的,系统再次重启后同样会遇到问题,需要永久性禁用`nouveau`来解决这个问题.

1. 禁用nouveau
```
1)把驱动加入黑名单中: /etc/modprobe.d/blacklist.conf 在后面加入：
 
    blacklist nouveau
 
    options nouveau modeset=0
 
2) 使用 dracut重新建立 initramfs nouveau 并且备份 initramfs nouveau image镜像
 
    mv /boot/initramfs-$(uname -r).img /boot/initramfs-$(uname -r).img.bak
 
3) 重新建立新的 the initramfs file
 
    dracut -v /boot/initramfs-$(uname -r).img $(uname -r)
 
4)重启，检查nouveau driver确保没有被加载！
 
    reboot
 
    lsmod | grep nouveau
```

2. 安装NVIDIA 官方驱动
参考CentOS安装Nvidia GPU驱动文档,不再赘述

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。