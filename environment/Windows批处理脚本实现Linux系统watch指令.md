---
title: Windows批处理脚本实现Linux系统watch指令
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---


脚本如下：
```
@ECHO OFF
:loop
  cls
  %*
  timeout /t 1 > NUL
goto loop
```
使用方法：保存脚本至某位置，例如`d:\scripts\watch.bat`,添加父级目录到环境变量，即可使用命令行查看，示例如下:

> 注: `linux`指令支持输入间隔时间,如`watch -n 1 nvidia-smi` 表示每个1秒执行一次，此处的间隔时间硬编码在脚本中，使用`/t`参数指定
```
watch nvidia-smi 

## 输出如下:


Tue Nov  8 15:40:37 2022
+-----------------------------------------------------------------------------+
| NVIDIA-SMI 517.48       Driver Version: 517.48       CUDA Version: 11.7     |
|-------------------------------+----------------------+----------------------+
| GPU  Name            TCC/WDDM | Bus-Id        Disp.A | Volatile Uncorr. ECC |
| Fan  Temp  Perf  Pwr:Usage/Cap|         Memory-Usage | GPU-Util  Compute M. |
|                               |                      |               MIG M. |
|===============================+======================+======================|
|   0  NVIDIA GeForce ... WDDM  | 00000000:01:00.0  On |                  N/A |
| 21%   37C    P8    12W / 125W |   1075MiB /  6144MiB |     19%      Default |
|                               |                      |                  N/A |
+-------------------------------+----------------------+----------------------+

+-----------------------------------------------------------------------------+
| Processes:                                                                  |
|  GPU   GI   CI        PID   Type   Process name                  GPU Memory |
|        ID   ID                                                   Usage      |
|=============================================================================|
|    0   N/A  N/A      1144    C+G   ...icrosoft VS Code\Code.exe    N/A      |
|    0   N/A  N/A      1848    C+G   ...bbwe\Microsoft.Photos.exe    N/A      |
|    0   N/A  N/A      2560    C+G   ...3\jbr\bin\jcef_helper.exe    N/A      |
|    0   N/A  N/A      3944    C+G   ...me\Application\chrome.exe    N/A      |
|    0   N/A  N/A     15956    C+G   ...y\ShellExperienceHost.exe    N/A      |
|    0   N/A  N/A     17140    C+G   ...kyb3d8bbwe\Calculator.exe    N/A      |
|    0   N/A  N/A     18136    C+G   D:\VMWare\x64\mksSandbox.exe    N/A      |
|    0   N/A  N/A     19336    C+G   C:\Windows\explorer.exe         N/A      |
+-----------------------------------------------------------------------------+
```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。