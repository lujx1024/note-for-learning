---
title: CentOS安装FFmpeg环境及解码器
tags: CentOS,FFmpeg,安装
renderNumberedHeading: true
grammar_cjkRuby: true
---

[TOC]
# 编译与安装说明

本篇说明文档基于最新版本的CentOS的最简安装，将提供本地非系统及级别的FFmpeg安装流程，并支持几个通用的外部解码器。本篇安装说明同样适用于最新版本的红帽(RHEL)系统和Fedora系统。

关于编译软件编译的其他信息，您可以参考通用编译指南，[参考链接](https://trac.ffmpeg.org/wiki/GenericCompilationGuide)

本文档所设计的安装方法是非侵入型的，需要在您本地创建几个文件夹：
- ffmpeg_sources  – 用于保存安装时下载的源代码文件，安装完成后可删除。
- ffmpeg_build       – 用于保存源代码编译后的文件及依赖库的安装，安装完成后可删除。
- bin                       – 软件和解码器等安装位置,如(ffmpeg, ffprobe, x264, x265)等。

参考[还原更改](https://trac.ffmpeg.org/wiki/CompilationGuide/Centos#RevertingChangesmadebythisGuide)，您可以撤销本指南中任意一步操作。

> **==温馨提示： #4CAF50==**  如果您不方便或因其他原因无法进行源码编译，可直接下载最新的预编译安装包 [下载链接](https://ffmpeg.org/download.html)

# 安装环境依赖

> **====说明： #2196F3== #FFEB3B==** 指令代码中的 # 号表示该指令需使用超级权限用户或`root`用户执行，在本文中，`yum`指令必须使用超级权限用户执行

## 安装依赖
安装必要的系统依赖，以下是源码编译与安装时所必须的依赖库：
```
# yum install autoconf automake bzip2 bzip2-devel cmake freetype-devel gcc gcc-c++ git libtool make pkgconfig zlib-devel
```

## 创建文件夹
在用户`家目录`创建一个新的文件夹，用于保存`FFmpeg`以及`解码器`的源代码
`mkdir ~/ffmpeg_sources`

# 源代码下载、编译与安装

> **==温馨提示： #4CAF50==** ==如果您不需要安装所有的解码器，只需要跳过相应的解码器安装模块，移除安装`FFmpeg`时`./configure` 的对应参数即可，例如，如果不需要安装 `libvpx`, 则跳过此解码器的安装流程，然后删除 `--enable-libvpx` 配置参数即可. #4CAF50==

## 安装 NASM 

`NASM`是系统中某些依赖库会使用的编译器，强烈建议安装，否则在接下来的安装编译过程会很耗时。

```
cd ~/ffmpeg_sources
curl -O -L https://www.nasm.us/pub/nasm/releasebuilds/2.15.05/nasm-2.15.05.tar.bz2
tar xjvf nasm-2.15.05.tar.bz2
cd nasm-2.15.05
./autogen.sh
./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin"
make
make install
```

## 安装 Yasm
同上 , `Yasm`是系统中某些依赖库会使用的编译器，强烈建议安装，否则在接下来的安装编译过程会很耗时。
```
cd ~/ffmpeg_sources
curl -O -L https://www.tortall.net/projects/yasm/releases/yasm-1.3.0.tar.gz
tar xzvf yasm-1.3.0.tar.gz
cd yasm-1.3.0
./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin"
make
make install
```

## 安装 libx264

H.264 视频解码器，详情及使用方法请点击[参考链接](https://trac.ffmpeg.org/wiki/Encode/H.264)

安装 `ffmpeg`时需配置`--enable-gpl` `--enable-libx264`.
```
cd ~/ffmpeg_sources
git clone --branch stable --depth 1 https://code.videolan.org/videolan/x264.git
cd x264
PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin" --enable-static
make
make install
```

> **==Warning: #F44336==** ==If you get Found no assembler. Minimum version is nasm-2.13 or similar after running ./configure then the outdated nasm package from the repo is installed. Run yum remove nasm && hash -d nasm and x264 will then use your newly compiled nasm instead. Ensure environment is able to resolve path to nasm binary. #E91E63==

## 安装 libx265
H.265/HEVC  视频解码器，详情及使用方法请点击[参考链接](https://trac.ffmpeg.org/wiki/Encode/H.265)

安装 `ffmpeg`时需配置`--enable-gpl` `--enable-libx265`.

```
cd ~/ffmpeg_sources
git clone --branch stable --depth 2 https://bitbucket.org/multicoreware/x265_git
cd ~/ffmpeg_sources/x265_git/build/linux
cmake -G "Unix Makefiles" -DCMAKE_INSTALL_PREFIX="$HOME/ffmpeg_build" -DENABLE_SHARED:bool=off ../../source
make
make install
```

## 安装 libfdk_aac
AAC 音频解码器，详情及使用方法请点击[参考链接](https://trac.ffmpeg.org/wiki/Encode/AAC)

安装 `ffmpeg`时需配置`--enable-libfdk_aac`(如果您同样配置了`--enable-gpl`，需再加上`--enable-nonfree`)

```
cd ~/ffmpeg_sources
git clone --depth 1 https://github.com/mstorsjo/fdk-aac
cd fdk-aac
autoreconf -fiv
./configure --prefix="$HOME/ffmpeg_build" --disable-shared
make
make install
```

## 安装 libmp3lame
MP3 音频解码器

安装 `ffmpeg`时需配置`--enable-libmp3lame`

```
cd ~/ffmpeg_sources
curl -O -L https://downloads.sourceforge.net/project/lame/lame/3.100/lame-3.100.tar.gz
tar xzvf lame-3.100.tar.gz
cd lame-3.100
./configure --prefix="$HOME/ffmpeg_build" --bindir="$HOME/bin" --disable-shared --enable-nasm
make
make install
```

## 安装 libopus
Opus 音频编码与解码器.

安装 `ffmpeg`时需配置`--enable-libopus`

```
cd ~/ffmpeg_sources
curl -O -L https://archive.mozilla.org/pub/opus/opus-1.3.1.tar.gz
tar xzvf opus-1.3.1.tar.gz
cd opus-1.3.1
./configure --prefix="$HOME/ffmpeg_build" --disable-shared
make
make install
```

## 安装 libvpx
VP8/VP9 视频编码与解码器.详情及使用方法请点击[参考链接](https://trac.ffmpeg.org/wiki/Encode/VP9)

安装 `ffmpeg`时需配置`--enable-libvpx`

```
cd ~/ffmpeg_sources
git clone --depth 1 https://chromium.googlesource.com/webm/libvpx.git
cd libvpx
./configure --prefix="$HOME/ffmpeg_build" --disable-examples --disable-unit-tests --enable-vp9-highbitdepth --as=yasm
make
make install
```

> > **==温馨提示： #4CAF50==** ==google资源下载可能会出现连接超时或资源下载速度过慢等问题导致安装失败，建议使用其他方式(如浏览器+科学上网等)下载源码后，将源码上传到gitee或github后，将原始链接更换为新链接后再执行下载、编译安装等操作 #4CAF50==

## 安装 ffmpeg

```
cd ~/ffmpeg_sources
curl -O -L https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2
tar xjvf ffmpeg-snapshot.tar.bz2
cd ffmpeg
PATH="$HOME/bin:$PATH" PKG_CONFIG_PATH="$HOME/ffmpeg_build/lib/pkgconfig" ./configure \
  --prefix="$HOME/ffmpeg_build" \
  --pkg-config-flags="--static" \
  --extra-cflags="-I$HOME/ffmpeg_build/include" \
  --extra-ldflags="-L$HOME/ffmpeg_build/lib" \
  --extra-libs=-lpthread \
  --extra-libs=-lm \
  --bindir="$HOME/bin" \
  --enable-gpl \
  --enable-libfdk_aac \
  --enable-libfreetype \
  --enable-libmp3lame \
  --enable-libopus \
  --enable-libvpx \
  --enable-libx264 \
  --enable-libx265 \
  --enable-nonfree
make
make install
hash -d ffmpeg
```

至此，`FFmpeg`及其部分解码器的安装流程就全部结束了。下面的内容是关于如何更新和移除已安装的软件或依赖库，如有需要，您继续往下看。

# 更新

FFmpeg 仍处于开发中，并且时常会有版本更新和异常修复版本，更新操作需要首先移除旧版本文件，在更新依赖库文件：

```
rm -rf ~/ffmpeg_build ~/bin/{ffmpeg,ffprobe,lame,x264,x265}
# yum install autoconf automake bzip2 bzip2-devel cmake freetype-devel gcc gcc-c++ git libtool make mercurial pkgconfig zlib-devel
```

## 更新 x264

```
cd ~/ffmpeg_sources/x264
make distclean
git pull
```

Then run` ./configure`, `make`, and `make install` as shown in the` Install x264 `section.


## 更新 x265

```
cd ~/ffmpeg_sources/x265_git
rm -rf ~/ffmpeg_sources/x265_git/build/linux/*
git pull
cd ~/ffmpeg_sources/x265_git/build/linux
```
Then run `cmake`, `make`, and `make install` as shown in the` Install x265 `section.

## 更新 libfdk_aac

```
cd ~/ffmpeg_sources/fdk_aac
make distclean
git pull
```
Then run` ./configure`, `make`, and `make install` as shown in the` Install libfdk_aac` section.

## 更新 libvpx

```
cd ~/ffmpeg_sources/libvpx
make distclean
git pull
```
Then run `./configure`, `make`, and `make install` as shown in the `Install libvpx` section.

## 更新 FFmpeg

```
rm -rf ~/ffmpeg_sources/ffmpeg
```
重新运行 `Install FFmpeg` 部分.

## 撤销此文档的所有安装

```
rm -rf ~/ffmpeg_build ~/ffmpeg_sources ~/bin/{ffmpeg,ffprobe,lame,nasm,vsyasm,x264,yasm,ytasm}
# yum erase autoconf automake bzip2 bzip2-devel cmake freetype-devel gcc gcc-c++ git libtool zlib-devel
hash -r
```



欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。