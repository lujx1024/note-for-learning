---
title: Python项目打包EXE
tags: Python,EXE,PyInstaller
renderNumberedHeading: true
grammar_cjkRuby: true
---

[toc!?depth=3]

* [概述](#概述)
* [使用方法](#使用方法)
	* [安装](#安装)
	* [单文件打包](#单文件打包)
	* [项目多文件打包](#项目多文件打包)
		* [项目结构](#项目结构)
		* [生成打包配置文件](#生成打包配置文件)
		* [打包为EXE](#打包为exe)
	* [TroubleShooting](#troubleshooting)
		* [文件的路径问题](#文件的路径问题)
		* [打包文件报错：](#打包文件报错)
		* [更换图标报错：](#更换图标报错)
		* [打包错误：](#打包错误)
		* [运行exe文件报错：](#运行exe文件报错)
		* [文件打包后过大](#文件打包后过大)
* [参考链接](#参考链接)

# 概述

`PyInstaller`将`Python`应用程序及其所有依赖项打包到一个包中。用户可以在不安装`Python解释器`或任何模块的情况下运行打包的`EXE`应用程序。`PyInstaller`支持`Python 3.7`及以上版本，并成功支持了许多主流的第三方`Python`包，如`numpy`、`matplotlib`、`PyQt`、`wxPython`等。



`PyInstaller`在`Windows`、`MacOS X`和`Linux`上进行了测试。但它并非是交叉编译器;如要在`Windows`上运行一个`Windows`应用程序，要在`Linux`上运行一个`Linux`应用程序等.`x PyInstaller`已经在`AIX`, `Solaris`, `FreeBSD`和`OpenBSD`上成功使用。

# 使用方法

## 安装

`pyinstaller`可直接通过`pip`安装,如下所示：
```
pip install -U pyinstaller
```

## 单文件打包
启动命令行界面，激活虚拟环境，切换到待打包的文件路径，执行打包指令，如下:
```
pyinstaller your_program.py
```
打包过程中会输出日志，待打包完成后，会生成`build` `dist`两个文件夹和`your_program.spec`配置文件，输出的`EXE`文件位于`dist`文件夹内，直接双击即可运行。
> 注：除`exe`文件外，生成的其他临时文件均可删除


## 项目多文件打包

### 项目结构
对于包含多文件和静态资源如图片、文本、模型等的Python项目，需要将包括第三方依赖、代码文件、静态资源文件等一起打包，以下面的项目结构为例，

```
test_installer
|--resources            # 静态资源文件夹
|--random_rectangle.py     # 工具类代码文件
|--video_player.py        # 项目主运行文件
```
如上所示，`resources`为静态资源文件夹,可放置图片、文本、深度学习模型等数据，可以使子文件或子文件夹，`random_rectangle.py`为依赖文件，如一些公共类或公共方法，`video_player.py`为项目入口文件，即主运行文件，激活虚拟环境后执行`python video_player.py`即可启动项目。

### 生成打包配置文件
使用`pyi-makespec`指令生成spec配置文件，如下：
```
pyi-makespec -w xxx.py

## xxx.py文件为要执行的主文件，这里为video_player.py
```

打开生成的spec文件，将需要打包的其他文件写入配置中:

> 注：主要需要关注与修改的配置  : Analysis的Python文件列表、pathex、datas

> 注：windows系统，使用不含中文字符的绝对路径，且使用双反斜杠`\\`

```
# -*- mode: python ; coding: utf-8 -*-
# 当出现出现"RecursionError: maximum recursion depth exceeded问题时，
# 可能打包时出现了大量的递归超出了python预设的递归深度，需要添加如下三行。
import sys
import os.path as osp
sys.setrecursionlimit(5000)
#----------------------------------------------------------------

block_cipher = None


a = Analysis(
	# 所有项目中的py文件路径以列表形式写入Analysis,如下:
    ['video_player.py','random_rectangle.py'],
	# 项目路径
    pathex=[E:\\python\\python_project\\test_installer],
	# 程序调用外部pyd、dll文件（二进制文件路径）以数组形式传入;
	# 例:('D:\\pro\\text.dll', 'pro'),将'pdftotext.dll'pro，与原项目结构一致即可
    binaries=[],
	# 存放的资源文件（图片、文本等静态文件）以数组形成传入;
	# 例：('D:\\static\\c.ioc','static'),将'cc.ioc'打包之后放在static目录，与原项目结构一致即可
    datas=[('E:\\python\\python_project\\test_installer\\resources','resources')],
	# pyinstaller解析模块时可能会遗漏某些模块（not visible to the analysis phase），
	# 造成打包后执行程序时出现类似No Module named xxx;这时就需要在hiddenimports中加入遗漏的模块
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[], # 去除不必要的模块import，写在excludes中添加此模块
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

# .pyz的压缩包，包含程序运行需要的所有依赖
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

# 根据Analysis和PYZ生成单个exe程序所需要的属性及其配置
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='video_player',  # 生成exe文件的名字
    debug=False, # debug模式
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False, # 是否在打开exe文件时打开cmd命令框 
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
	icon='' # 设置exe程序图标，ico格式文件（16*16）
)

# 收集前三个部分的内容进行整合，生成程序所需要的依赖包，及资源文件和配置
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='video_player',
)

```

### 打包为EXE
同上，激活虚拟环境，切换到正确的目录，执行以下指令(如果生成spec的窗口没有关闭，可以直接在同一个窗口运行)：
```
pyinstaller  xxx.spec
# 或者
pyinstaller -D xxx.spec
```
> 注：不同的机器运行的指令有差异，如果其中一个报错，运行另一个即可

运行完成后，同样生成`build`和`dist`两个文件夹，EXE文件位于`dist`文件夹中，`build`文件夹则可以删除。


## TroubleShooting

### `spec`文件的路径问题
- WIndows系统 : 使用绝对路径；使用双反斜杠`\\`;不使用中文字符.示例：`E:\\python\\projects`
- Linux系统 :  使用绝对路径；不使用中文字符.示例：`/home/python/projects`
  
### 打包`spec`文件报错：`RecursionError: maximum recursion depth exceeded`

   当出现`RecursionError: maximum recursion depth exceeded`问题时，可能打包时出现了大量的递归超出了`python`预设的递归深度，需要添加如下三行 :
	```
	import sys
	import os.path as osp
	sys.setrecursionlimit(5000)
	```
### 更换`exe`图标报错：`AttributeError: module 'win32ctypes.pywin32.win32api' has no attribute 'error`
- 图标的大小建议（64*64）:[网址](https://lvwenhan.com/convertico/)
- 图标的颜色严格限制：256，真彩色是不行的

### 打包错误：`ModuleNotFoundError: No module named 'xxxxx'`

- 方法1：pyinstaller -D --hidden-import="xxxxx" main.py
- 方法2：在xxx.spec中配置hiddenimports=['xxxxx']

### 运行exe文件报错：`Failed to excute Script main`
 使用-c模式重新打包调试，找的缺失的模块，`pip install`安装

### 文件打包后过大
 在程序中尽量不使用`import xx`；而是使用` from xx import xx`

# 参考链接
- 【简 书】[python使用Pyinstaller打包整个项目](https://www.jianshu.com/p/3e62c7449fd1)
- 【博客园】[PyInstaller打包Python项目详解 ](https://www.cnblogs.com/bbiu/p/13209612.html)
- 【官方文档】[PyInstaller Documentation](https://pyinstaller.org/en/stable/index.html)


欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。