---
title: Linux同步系统时间
tags: Linux,时间同步,定时任务
renderNumberedHeading: true
grammar_cjkRuby: true
---

##  ntpdate同步时间
### 手动同步时间
```
[root@node1 ~]# ntpdate cn.pool.ntp.org
 3 Jun 18:06:16 ntpdate[2317]: adjust time server 202.112.29.82 offset -0.007719 sec
 ```
> 注意：如果会出现以下提示：no server suitable for synchronization found.加入-u参数，来同步时间
```
ntpdate -u cn.pool.ntp.org
```
时间同步完成后，执行命令`hwclock -w`,将当前系统时间写入`BIOS`。另外`hwclock -r`可读取`BIOS`中的时间

###  配置定时任务，同步时间
```
[root@node1 ~]# crontab -e
# 每过半个小时同步一次
0 */30 * * * /usr/sbin/ntpdate -u cn.pool.ntp.org > /dev/null 2>&1; /sbin/hwclock -w
```
### 配置开启启动校验
编辑`/etc/rc.d/rc.local`文件(`vim /etc/rc.d/rc.local`),在文件末尾添加如下内容
```
/usr/sbin/ntpdate -u cn.pool.ntp.org> /dev/null 2>&1; /sbin/hwclock -w
```


欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。