---
title: CentOS升级gcc版本
tags: CentOS,GCC,版本升级
renderNumberedHeading: true
grammar_cjkRuby: true
---
# 概述

`CentOS`系统使用`yum`安装的`gcc`版本默认为`gcc 4.8.5`, 当需要编译某些软件如`opencv`或`Paddle`时，会提示`当前gcc不支持c++ 11`导致编译失败，此时需要将`gcc`版本升级，本文档记录将`gcc 4.8.5 `升级至` gcc 7.5`的操作过程。

# 环境准备
## 安装依赖
首先需要安装包括低版本gcc在内的所有依赖库，提供源码编译等支持
`yum install -y glibc-headers gcc-c++  gcc gmp  gmp-devel  mpfr  mpfr-devel  libmpc  libmpc-devel`

## 源码下载

建议使用[官方网站](https://gcc.gnu.org/)，选择适合的版本下载，本次安装的是gcc 7.5，gcc官方网站提供了很多镜像站提供加速下载，选择适合的站点下载即可。

`wget http://mirrors.concertpass.com/gcc/releases/gcc-7.5.0/gcc-7.5.0.tar.gz` 

# 编译安装
## 解压文件

```
tar zxvf gcc-7.5.0.tar.gz
cd gcc-7.5.0
```

## 运行依赖安装脚本
`./contrib/download_prerequisites`

## 配置安装参数
```
mkdir build
cd build
../configure --prefix=/usr/local/gcc-7.5.0/ --enable-checking=release --enable-languages=c,c++ --disable-multilib
```

> `configure`是一个可执行脚本，它有很多选项，在待安装的源码路径下使用命令`./configure –help`输出详细的选项列表。
> - 其中`--prefix`选项是配置`安装路径`,如果不配置` --prefix `选项，安装后可执行文件默认放在`/usr /local/bin`
> - 库文件默认放在`/usr/local/lib`
> - 配置文件默认放在`/usr/local/etc`
> - 其它的资源文件放在`/usr /local/share`

> configure各项参数详解：
>>` --prefix=/usr/local/gcc-7.5.0/`：把所有资源文件都放在该路径下。
>> `--enable-checking=release`：生成的编译器在编译过程中不做额外检查。
>>`--enable-languages=c,c++`：让gcc支持c，c++。
>> `--disable-multilib`：不生成编译为其他平台可执行代码的交叉编译器。

## 编译
`make`
> 这个会耗时很久,超过一个小时，可以添加` -j`参数使用多线程编译，如` -j16` 使用`16线程`进行编译，线程数建议不超过CPU核心数，可使用`nproc`查看CPU核心数

## 安装
`make install`

> 这里同样可以使用`-j`参数加速

# 处理环境变量
上述make和make install如果没有报错，说明gcc 7.5.0已经安装成功，剩下的工作就是处理环境变量。

## 移除旧版本gcc
`yum remove gcc -y`

## 创建新版本gcc软连接

```
ln -sv /usr/local/gcc-7.5.0/bin/gcc /usr/bin/gcc
ln -sv /usr/local/gcc-7.5.0/bin/g++ /usr/bin/g++

```
## 添加环境变量
在`/etc/profile`中添加`LD_LIBRARY_PATH`环境变量,如下代码：
```
# gcc
LD_LIBRARY_PATH=/usr/local/gcc-9.3.0/lib
#export LD_LIBRARY_PATH
```
执行如下指令重新加载配置 :

`source /etc/profile`

## 更换so文件与相关软连接
```
cp /usr/local/gcc-7.5.0/lib64/libstdc++.so.6.0.24 /usr/lib64/libstdc++.so.6.0.24
rm -f /usr/lib64/libstdc++.so.6
ln -s /usr/lib64/libstdc++.so.6.0.24 /usr/lib64/libstdc++.so.6
```

[参考链接](https://www.jianshu.com/p/1817b01c437f)

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。