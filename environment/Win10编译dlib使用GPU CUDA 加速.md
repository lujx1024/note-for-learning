---
title: Win10编译dlib使用GPU CUDA 加速
tags: dlib,CUDA,环境部署
renderNumberedHeading: true
grammar_cjkRuby: true
---

# 环境准备

1. 操作系统:windows 10 
2. Microsoft Visual Studio 2019
3. CMake
4. Anaconda 或 python 3.5 以上环境
5. 已经正确安装CUDA和 cuDNN
6. dlib源代码

# 源码编译
##  下载dlib源代码
- 从[github地址](https://github.com/davisking/dlib) 下载源代码， 本实例中，下载的dlib版本号为`19.22`，故源代码文件夹为`dlib-19.22`,存放路径为`e:\dlib_cuda\dlib-19.22`
- 创建同级文件夹`build`
##  CMake编译源码
- 打开cmake-gui,`where is the source code`选择dlib源码位置,本实例中是`e:\dlib_cuda\dlib-19.22\dlib`(`github`下载的源代码文件的下一级目录)，
-  `where to build the binaries`选择上一步新建的文件夹`e:\dlib_cuda\build`,
-  点击`config`,选择`Visual Studio 2019`、`x64架构`点击Finish并等待完成即可

## python虚拟环境安装

- 进入anaconda或python虚拟环境，安装cmake依赖
 	`pip install cmake` 
- 命令行进入dlib-19.22文件夹，执行指令`python setup.py install`,这个过程需要进行源码的编译与安装，会占用CPU资源和几分钟的时间，等待安装结束即可

- 验证dlib安装是否成功
在命令行进入`python`，键入以下指令:
	```
	>>> import dlib
	>>> dlib.DLIB_USE_CUDA
	True
	
	结果显示为 True 即表示dlib安装成功
	```

# 编译时的报错问题

## error C2734: “GifAsciiTable8x8”
```
error C2734: “GifAsciiTable8x8”: 如果不是外部的，则必须初始化常量对象

 File "setup.py", line 134, in run
    self.build_extension(ext)
  File "setup.py", line 174, in build_extension
    subprocess.check_call(cmake_build, cwd=build_folder)
  File "D:\Anaconda3\lib\subprocess.py", line 364, in check_call
    raise CalledProcessError(retcode, cmd)
subprocess.CalledProcessError: Command '['cmake', '--build', '.', '--config', 'Release', '--', '/m']' returned non-zero exit status 1.

```

原因是：
CMake 在寻找计算机环境里面的 libfig库，没有找到。
解决方法：
可以不启用 `gif support`：
`python setup.py install --no DLIB_GIF_SUPPORT`


欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。 