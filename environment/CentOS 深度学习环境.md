---
title: CentOS 深度学习环境
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---

查看`CUDA`版本  `nvcc -V`

输出显示：

```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2019 NVIDIA Corporation
Built on Fri_Feb__8_19:08:17_PST_2019
Cuda compilation tools, release 10.1, V10.1.105
```
查看`cuDNN`版本 
`cat /usr/local/cuda/include/cudnn.h | grep CUDNN_MAJOR -A 2`
输出显示：

```

#define CUDNN_MAJOR 7
#define CUDNN_MINOR 6
#define CUDNN_PATCHLEVEL 5
--
#define CUDNN_VERSION (CUDNN_MAJOR * 1000 + CUDNN_MINOR * 100 + CUDNN_PATCHLEVEL)

#include "driver_types.h"
```

`CentOS`使用`Anaconda`换源
```
# 配置文件写在~/.condarc中 
# vim ~/.condarc
channels:
  - https://mirrors.ustc.edu.cn/anaconda/pkgs/main/
  - https://mirrors.ustc.edu.cn/anaconda/cloud/conda-forge/
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
  - defaults
```


欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。