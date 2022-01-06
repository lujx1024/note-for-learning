---
title: Windows安装python人脸识别依赖库dlib
tags: Python,dlib,环境
renderNumberedHeading: true
grammar_cjkRuby: true
---

# `dlib`概述
`Dlib`是一个包含机器学习算法的`C++`开源工具包。`Dlib`可以帮助您创建很多复杂的机器学习方面的软件来帮助解决实际问题。目前`Dlib`已经被广泛的用在行业和学术领域，包括机器人，嵌入式设备，移动电话和大型高性能计算环境.

# `pip`安装报错

`Windows`平台使用`pip`指令安装`dlib`依赖库时，往往会遇到报错问题，如下：
```
 Building wheel for dlib (setup.py) ... error 
  ERROR: Command errored out with exit status 1:
   command: 'd:\python36\python.exe' -u -c 'import io, os, sys, setuptools, 
   中间省略若干行...
  Complete output (8 lines):
  running bdist_wheel
  running build
  running build_py
  package init file 'tools\python\dlib\__init__.py' not found (or not a regular file)
  running build_ext
  ERROR: CMake must be installed to build dlib
  ----------------------------------------
  ERROR: Failed building wheel for dlib
```

# 安装方法

不同于各路大神介绍的使用CMake和VisualStudio编译源码的方式，pip工具直接前人已经编译好的二进制文件（扩展名为`.whl`）最为方便。

查看网址`https://pypi.org/simple/dlib/`，截止到本文档编写之日(20211110),列举出了适配python 3.6版本及以下以及python 2.x版本的二进制安装包文件 (最新版本的只有源码，没有二进制安装包)。

![dlib的pypi官方库](./images/1636528352367.png)

## `pip `工具安装

到这一步之后，使用pip工具有多种方式实现`dlib`的安装(由难到易):
1. 下载`whl`文件，打开命令行窗口,路径指向安装包同级目录，以`dlib19.8.1`为例，`pip install dliv-19.8.1-cp36-cp36m-win_amd64.whl` 即可完成安装 ;
2. 也可以不下载文件，通过右击鼠标获取对应包文件的链接，同样以`dlib19.8.1`为例，`pip install [文件链接]`，链接太长且不确定是否会变化，就不放在这儿了;
3. 直接指定安装有`whl`文件的对应版本号即可，如`pip install dlib==19.8.1`

`pypi`的官方库中，二进制文件只编译到了 `19.8.1-cp36`，对于python 3.7 和 3.8 等以上的版本没有最新的二进制安装包，这里记录一下`datamagic`大神编译的适配python3.7 python 3.8 以上的二进制安装包，[dlib for python 3.7 and above ](https://github.com/datamagic2020/Install-dlib),安装方式参考上方的步骤。


## `conda`工具安装

`conda `用户直接使用`conda install dlib` 即可。(别问我为啥，我也不知道，抱着试试看的心态测试一下，没想到一下就成功了)

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。