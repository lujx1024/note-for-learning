---
title: OpenVINO读取RTSP报错问题的解决
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---
# 概述
在已安装`OpenVINO`环境的`Windows`平台使用opencv读取本地视频文件或RTSP视频流时，遇到异常问题，报错信息:`Openvino MFX: Unsupported extension: rtsp://username:password@ip_addr:port/live/ch0` ,其原因在于本机未安装`ffmpeg`软件以及`OpenVINO 2020.3`自带的`OpenCV4.3`缺少`opencv_videoio_ffmpeg_64.dll`文件.
# ffmpeg安装

ffmpeg[官方下载链接](http://ffmpeg.org/download.html#build-windows)
windows平台全功能版本 [下载链接](https://www.gyan.dev/ffmpeg/builds/)
选择`ffmpeg-git-full`版本

配置环境变量

校验

```
ffmpeg version 2021-07-21-git-f614390ecc-full_build-www.gyan.dev Copyright (c) 2000-2021 the FFmpeg developers
built with gcc 10.3.0 (Rev5, Built by MSYS2 project)
configuration: --enable-gpl --enable-version3 --enable-static --disable-w32threads --disable-autodetect --enable-fontconfig --enable-iconv --enable-gnutls --enable-libxml2 --enable-gmp --enable-lzma --enable-libsnappy --enable-zlib --enable-librist --enable-libsrt --enable-libssh --enable-libzmq --enable-avisynth --enable-libbluray --enable-libcaca --enable-sdl2 --enable-libdav1d --enable-libzvbi --enable-librav1e --enable-libsvtav1 --enable-libwebp --enable-libx264 --enable-libx265 --enable-libxvid --enable-libaom --enable-libopenjpeg --enable-libvpx --enable-libass --enable-frei0r --enable-libfreetype --enable-libfribidi --enable-libvidstab --enable-libvmaf --enable-libzimg --enable-amf --enable-cuda-llvm --enable-cuvid --enable-ffnvcodec --enable-nvdec --enable-nvenc --enable-d3d11va --enable-dxva2 --enable-libmfx --enable-libglslang --enable-vulkan --enable-opencl --enable-libcdio --enable-libgme --enable-libmodplug --enable-libopenmpt --enable-libopencore-amrwb --enable-libmp3lame --enable-libshine --enable-libtheora --enable-libtwolame --enable-libvo-amrwbenc --enable-libilbc --enable-libgsm --enable-libopencore-amrnb --enable-libopus --enable-libspeex --enable-libvorbis --enable-ladspa --enable-libbs2b --enable-libflite --enable-libmysofa --enable-librubberband --enable-libsoxr --enable-chromaprint
libavutil      57.  1.100 / 57.  1.100
libavcodec     59.  3.102 / 59.  3.102
libavformat    59.  4.101 / 59.  4.101
libavdevice    59.  0.100 / 59.  0.100
libavfilter     8.  0.103 /  8.  0.103
libswscale      6.  0.100 /  6.  0.100
libswresample   4.  0.100 /  4.  0.100
libpostproc    56.  0.100 / 56.  0.100
```
OpenVino脚本下载下载动态链接库

脚本地址`C:\Program Files (x86)\Intel\openvino_2021\opencv\ffmpeg-download.ps1`

前三行
```
$url = "https://raw.githubusercontent.com/opencv/opencv_3rdparty/629590c3ba09fb0c8eaa9ab858ff13d3a84ca1aa/ffmpeg/opencv_videoio_ffmpeg_64.dll"
$expected_md5 = "7f10ae2e6a080ba3714f7a38ee03ae15"
$output = "$PSScriptRoot\bin\opencv_videoio_ffmpeg452_64.dll"
```
文件保存位置，(其他途径下载需要重命名文件为指定名称)
`C:\Program Files (x86)\Intel\openvino_2021\opencv\bin`





欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。