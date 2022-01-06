---
title: Linux系统挂载NTFS格式的硬盘或U盘
tags: linux,NTFS,挂载
renderNumberedHeading: true
grammar_cjkRuby: true
---
# 查看主机硬盘
使用`fdisk -l`查看主机硬盘情况，此时若NTFS格式的硬盘已接入，但未被挂载，使用`df -lh`无法查看存储情况。

使用`lsblk`查看物理硬盘，一般硬盘的命名顺序为 `sda`、`sdb `...

# 安装 NTFS-3G
1. 下载源码压缩包
	`wget http://tuxera.com/opensource/ntfs-3g_ntfsprogs-2017.3.23.tgz`
2. 解压
	`tar -zxvf ntfs-3g_ntfsprogs-2017.3.23.tgz`
3. 进入源码目录
	`cd ntfs-3g_ntfsprogs-2017.3.23/`
4. 创建安装目录
	`mkdir /usr/local/ntfs3g/`
5. 配置安装参数，指向新建安装目录
	`./configure --prefix=/usr/local/ntfs3g/`
6. 编译安装
	`make && make install`
7. 创建临时目录
	`mkdir /mnt/temp_ntfs`
8. 挂载硬盘到临时目录
	   `mount -t ntfs-3g /dev/sdb1 /mnt/temp_ntfs/`
	   机器重启后失效。
9. 解挂硬盘
	  `umount /dev/sdb1`
	  
# 实现开机自动挂载

要想实现自动开机挂载NTFS格式的USB硬盘，需要进行以下操作：

1. 首先备份fstab表
	`cp /etc/fstab /etc/fstabbakup`

2. 编辑`fstab`
	`vim /etc/fstab`
	在`fstab`表最后一行添加如下信息：
	`/dev/sdb1  /mnt/temp_ntfs/  ntfs-3g defaults 0 0`
	保存退出即可。

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。