---
title: CentOS 安装python人脸图像处理库 dlib
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---

安装百度`paddlepaddle`平台使用人脸图像处理工具过程中，用到了`dlib`依赖库，使用`pip`安装时遇到很多报错，这里记录一下安装方式与步骤

其中的一个报错：
```
CMake Error: The following variables are used in this project, but they are set to NOTFOUND.
Please set them or make sure they are set and tested correctly in the CMake files:
cusolver (ADVANCED)
    linked by target "dlib_shared" in directory /home/Downloads/dlib-19.6/dlib
    linked by target "dlib" in directory /home/Downloads/dlib-19.6/dlib
```


已成功的安装方式这里记录两种，其中`anaconda`的安装方式亲测通过，源码安装方式摘自博客，以供参考，无论以何种方式安装，都必须先安装`Linux依赖包`如`cmake`等。

### 安装依赖包

```
yum install build-essential cmake pkg-config -y
yum install build-essential cmake pkg-config -y
yum install libgtk-3-dev libboost-python-dev -y

```

### 使用`conda`安装

```
# 使用conda创建虚拟环境
conda create -n paddle python=3.6.8
conda activate paddle

# 安装依赖
conda install dlib

# 检查是否安装成功,进入 python 交互环境
(paddle) [root@localhost PaddleGAN]# python
Python 3.6.8 |Anaconda, Inc.| (default, Dec 30 2018, 01:22:34)
[GCC 7.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import dlib
>>> dlib.__version__
'19.21.0'
```

### 源码安装

```
# 下载源代码文件并解压
wget http://dlib.net/files/dlib-19.6.tar.bz2
tar xvf dlib-19.6.tar.bz2

# 编译 c++ 二进制文件
cd dlib-19.6/
mkdir build
cd build
cmake .. -DDLIB_USE_CUDA=1 -DUSE_AVX_INSTRUCTIONS=1 -DCUDA_NVCC_FLAGS="--expt-relaxed-constexpr"
cmake --build . --config Release
sudo make install
sudo ldconfig
cd ..

#  使用pkg-config配置并提供 Dlib的包含目录和链接Dlib库文件的路径
pkg-config --libs --cflags dlib-1

python setup.py install --set DLIB_USE_CUDA=1 --set USE_AVX_INSTRUCTIONS=1 --set CUDA_NVCC_FLAGS=" --expt-relaxed-constexpr" 

```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。