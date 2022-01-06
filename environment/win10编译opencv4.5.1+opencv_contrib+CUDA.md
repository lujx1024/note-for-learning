---
title: win10编译opencv4.5.1+opencv_contrib+CUDA
tags: OpenCV;CUDA;GPU加速
renderNumberedHeading: true
grammar_cjkRuby: true
---

# 准备工作

## 平台与软件

 - Windows10系统
- Visual Studio 2019：Visual Studio Community 2019
- Cmake：cmake-3.20.0-rc3-windows-x86_64.msi
- OpenCV 4.51：opencv-4.5.1.tar.gz
- OpenCV_contrib 4.5.1：opencv_contrib-4.5.1.tar.gz

## NVIDIA驱动、CUDA和cuDnn

选择适当的驱动和CUDA版本以及对应版本的cudnn，安装win10环境。

![![NVIDIA微架构、CUDA以及显卡型号对应关系](./images/1636164919238.png)](./images/1636164952078.png)

## 安装下载VS 2019、cmake和opencv及扩展模块源码

### VS 2019下载安装

[下载链接](https://visualstudio.microsoft.com/zh-hans/downloads/)

### cmake 下载安装

[下载链接](https://cmake.org/download/)

### opencv和opencv_contrib下载

[opencv下载链接](https://github.com/opencv/opencv)
[opencv_contrib](https://github.com/opencv/opencv_contrib)

[百度云下载](https://pan.baidu.com/s/1RUaNWtViExlJYVDShLpTTQ )
提取码：`lujx` 


> 注：点击左上角的Tag，选择4.5.4版本，opencv和opencv_contrib选择同样的版本

### 解压文件，准备就绪

创建`opencv_cuda`文件夹，将`opencv`和`opencv_contrib`解压到此文件夹中，并在opencv同级目录创建build文件夹。至此准备工作完成。
目录结构大致如下：
```
|-opencv_cuda
	|--build
	|--opencv_contrib_4.5.4
	|--opencv_4.5.4
		 |---.cache
		 |---其他原有的解压的子文件
	
```

> 为避免在首次编译过程中因文件下载失败导致编译不成功，需要将.cache文件夹复制到解压后的opencv源码文件夹中


# 编译OpenCV

## CMake 编译

1. 打开`cmake-gui`软件，分别将`where is the source code`和`where to build the binaries`添加为`opencv源码文件夹`和`build文件夹`
2. 第一次点击 `configure`, 选择`vs 2019`和`x64`架构，点击`finish`，开始第一次编译
3. 编译过程需要下载各种依赖，大概率会因为网络问题会卡住，直接复制.cache文件夹，可省去此烦恼
4. (此步选做) 创建虚拟环境，建议使用`anaconda`,并在虚拟环境中安装numpy(编译时需要),执行此步骤是为了将`CUDA版本`的opencv安装到`虚拟环境`中，`只安装到宿主机环境不需要执行此步骤`
5. (此步骤选做，但执行此步骤的前提是必须执行上一个步骤) 更换一下几个变量，分别将路径指向虚拟环境的对应位置 : `PYTHON3_EXECUTABLE`、`PYTHON3_INCLUDE_DIR`、`PYTHON3_LIBRARY`、`PYTHON3_NUMPY_INCLUDE_DIRS`、`PYTHON3_PACKAGES_PATH`
6.  编译完成后，在Search框内输入`CUDA`和`fast`，勾选三个配置 : `WITH_CUDA `、`OPENCV_DNN_CUDA`、`ENABLE_FAST_MATH`
7.  Search框搜`world`，将`build_opencv_world`打勾，将所有opencv的库都编译在一起不需要自己一一添加每个小模块。
8.  Search框搜`BUILD`，勾选`BUILD_opencv_python3`
9.  search框搜`MODULES`，在`OPENCV_EXTRA_MODULES_RATH`一项，添加`opencv_contrib4.5.1`中的`modules`目录
10.  search框搜`NON`，把`OPENCV_ENABLE_NONFREE `打勾
11.   第二次点击`configure`，等待下方日志显示`configure done`
12.   搜索框输入`cuda`，勾选`CUDA_FAST_MATH `，`CUDA_ARCH_BIN`中将显卡的算力内容改成自己显卡的算力，对应算力与显卡型号如第一章图片所示，如，显卡型号为 `GTX 1050`所对应的算力为`6.1`，则删除其他的算力版本，仅保留`6.1`即可
13.  再次点击configure，这次的Configuring done终于OK，然后点击Generate，稍等片刻出现Generating done！
14. 点击Open Project，它会启动你的Visual Studio。

## VS 编译
1. VS2019打开刚刚编译工程后，会反应一段时间，一定要等待左下角显示的项全部加载完毕才可以继续操作
  
2. 选择`Release ``x64`，接着找到`CmakeTargets`下的`ALL_BUILD`，右键→“生成”，然后开始漫长的等待……（笔记本 i7-9750H编译约65分钟，仅供参考）

3. `解决方案资源管理器`—>`CMakeTargets`—>`INSTALL`—>`生成`”然后又是等，好在这次时间很短。此时`opencv_cuda\build\lib\python3\Release`文件夹下可以看到`cv2.cp36-win_amd64.pyd`文件(不同的python版本，名称会略有差异)


4. 同时，在虚拟环境或者宿主机环境中，可以在路径`Lib\site-packages`下看到`cv2`文件夹
 
 
 ## 验证opencv环境
 使用命令行进入python环境,执行一下代码即可验证:
 ```
 c:\users\administrator> python
 >>> import cv2
 >>> cv2.cuda.getCudaEnabledDeviceCount()
 1 # 得到GPU设备数量，即表示opencv的GPU版本已经安装成功
 ```
 
 
欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。