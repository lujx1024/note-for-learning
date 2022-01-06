---
title: Linux多线程快速压缩解压文件
tags: CentOs,多线程,压缩解压
renderNumberedHeading: true
grammar_cjkRuby: true
---

# 使用多核心或多线程`CPU`加速`tar`压缩操作
在大多数`类UNIX`系统中，`tar`被应用于打包压缩的工具，内置在几乎所有的`通用Linux`或`BSD`发行版Linux系统中，然而，`tar`在压缩文件时通常耗时较长，因为它不支持多线程压缩，但是, tar支持指定外部压缩程序执行压缩操作，因此在压缩文件时，可选择支持多线程的压缩程序来提高压缩速度。
查看tar的参数表，可知：
```
-I, –use-compress-program PROG
filter through PROG (must accept -d)
```
使用参数`-I`或 `--use-compress-program`,可以指定其他的压缩程序。

这里记录三个并行压缩工具，三者都可在基于GNU的Debian或Ubuntu平台通过`apt install`指令或Redhat、CentOS平台通过`yum install`指令安装。

以下是压缩指令以及该指令所对应的安装包名称
 - **gz** : `pigz`
- **bz2** :  `pbzip2`
- **xz** :  `pxz `, `pixz`
> 注: 新版本 Ubuntu 和 Debian 不在支持 pxz , 但是pixz可完成同样功能

原始的压缩指令如下所示：

- gz :  ` tar -czf tarball.tgz files`
- bz2 :  `tar -cjf tarball.tbz files`
- xz : ` tar -cJf tarball.txz files`

多线程指令:

- gz:   `tar -I pigz -cf tarball.tgz files`
- bz2: `tar -I pbzip2 -cf tarball.tbz files`
- xz:   `tar -I pixz -cf tarball.txz files`
- xz:   `tar -I pxz -cf tarball.txz files`

上述多线程指令，`-I` 参数所指向的压缩程序，使用的都是默认参数，指定参数运行如`压缩级别`、`线程数`等，须执行如下指令：

`tar -c -I 'xz -9 -T0' -f archive.tar.xz [list of files and folders]`

打包文件夹为压缩文件时，使用如下指令:
`tar -cf -  list of files and folders| xz -9 -T0 >| archive.tar.xz`

> 可通过执行对应程序的`help`指令了解参数具体含义，如 `xz --help`可查询`-9` `-T0`等参数分别代表使用`压缩级别9`和`全部的CPU线程资源`


欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。