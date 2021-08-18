---
title: 人数识别CPU平台环境部署
tags: Python,PaddlePaddle,环境安装
renderNumberedHeading: true
grammar_cjkRuby: true
---
[TOC]
# Python安装
为保证系统与框架及环境的兼容性，`python`环境选择使用`3.6.8`版本.
## 下载
下载历史版本`Python 3.6.8 `，[网站链接](https://www.python.org/downloads/release/python-368/)，选择对应`windows`版本下载即可，安装包全名是`python-3.6.8-amd64.exe`
## 安装
安装方式同其他软件，双击安装程序，勾选`Add Python 3.x to PATH`，可自定义安装路径，也可使用默认安装路径，然后点击下一步知道安装结束即可。

## pip永久更换源
1. 在用户文件夹创建pip文件夹
	这个文件夹名是每个人的电脑环境不同而不同，例如我的地址是`C:\Users\aoto`,有的是`C:\Users\Administrator`
2. 新建`pip.ini`文件，键入以下内容，保存关闭即可
```
[global]
index-url=https://pypi.douban.com/simple/
[install]
trusted-host=pypi.douban.com
```

# 创建虚拟环境
## 安装虚拟环境管理工具
`pip install virtualenvwrapper-win`

## 配置环境变量
配置环境变量的目的主要是，在虚拟环境管理工具创建新的虚拟环境时，使用环境变量指定的路径保存依赖包和安装文件，如果不配置，默认保存在C盘对应的用户文件夹下，此处强烈建议配置环境变量以便管理。
环境变量名:`WORKON_HOME`
环境环境变量值：`E:\workon_home`

> 注：环境变量名为强制命名，不可变，必须是`WORKON_HOME`；环境变量值所对应的路径根据实际情况和需要自行设定

## 创建虚拟环境
`mkvirtualenv yolo`
# 安装PaddlePaddle框架
## Paddle安装
`PaddlePaddle`框架的安装，官方网站有比较详细的介绍，[参考链接](https://www.paddlepaddle.org.cn/install/quick?docurl=/documentation/docs/zh/install/pip/windows-pip.html)
进入官网后，依次选择`飞桨版本`、`操作系统`、`安装方式`、`计算平台`，复制下方生成的`链接`，在已经创建好的虚拟环境安装即可。
本实例，所选择的配置是飞桨版本` 2.1`、`Windows `操作系统、`pip `安装方式以及 `CPU 版本`计算平台，安装链接`python -m pip install paddlepaddle -i https://mirror.baidu.com/pypi/simple`

## Paddle环境校验
安装命令执行完成后，需进入`虚拟环境`的`python`环境中校验是否安装成功，在校验之前，由于此次安装是在`Windows`平台上，所以需要安装`VC_redist.x64.exe`
安装完成后，首先进入虚拟环境，再使用python指令进入python环境，导入paddle依赖后，执行测试方法，指令如下：
```
# 进入虚拟环境
C:\Users\aoto>workon yolo

# 进入python环境
(yolo) C:\Users\aoto>python
Python 3.6.8 (tags/v3.6.8:3c6b436a57, Dec 24 2018, 00:16:47) [MSC v.1916 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.

# 导入paddle依赖，如没有安装VC_redist，此步操作报错
>>> import paddle

# 运行检测方法
>>> paddle.utils.run_check()

# 输出检测结果
Running verify PaddlePaddle program ...
PaddlePaddle works well on 1 CPU.
W0713 14:41:51.268666  9472 fuse_all_reduce_op_pass.cc:76] Find all_reduce operators: 2. To make the speed faster, some all_reduce ops are fused during training, after fusion, the number of all_reduce ops is 2.
PaddlePaddle works well on 2 CPUs.
PaddlePaddle is installed successfully! Let's start deep learning with PaddlePaddle now.
```
# 安装PaddleDetection框架
以下为`PaddleDetection`的简单安装说明，详细说明文档请参考`PaddleDetection`框架[官方文档](https://github.com/PaddlePaddle/PaddleDetection/blob/release/2.1/docs/tutorials/INSTALL_cn.md)

## 安装依赖
确保`PaddlePaddle`框架已安装成功,安装`Microsoft C++ Build Tools`或者 `Visual Studio 2019`选择`C++` 模块,等待安装完成后，执行PaddleDetection的安装

## 安装detection
```
# pip安装paddledet
pip install paddledet==2.1.0 -i https://mirror.baidu.com/pypi/simple

# 下载使用源码中的配置文件和代码示例
git clone https://github.com/PaddlePaddle/PaddleDetection.git

# 编译安装paddledet
cd PaddleDetection
python setup.py install

# 安装其他依赖
pip install -r requirements.txt
```
## 安装校验
安装后确认测试通过：
`python ppdet/modeling/tests/test_architectures.py`

测试通过后会提示如下信息：
```
.....
----------------------------------------------------------------------
Ran 5 tests in 4.280s
OK
```
## 快速体验
在CPU上预测一张图片
```
python tools/infer.py -c configs/ppyolo/ppyolo_r50vd_dcn_1x_coco.yml -o use_gpu=false weights=https://paddledet.bj.bcebos.com/models/ppyolo_r50vd_dcn_1x_coco.pdparams --infer_img=demo/000000014439.jpg
```
会在`output`文件夹下生成一个画有预测结果的同名图像。
# 安装PaddleX框架

## 快速安装
以下安装过程默认用户已安装好`paddlepaddle-gpu`或`paddlepaddle`(版本大于或等于1.8.1)，`paddlepaddle`安装方式参照上文或者[飞桨官网](https://www.paddlepaddle.org.cn/)

##  pip安装
注意其中`pycocotools`在`Windows`安装较为特殊，可参考下面的`Windows`安装命令
`pip install paddlex -i https://mirror.baidu.com/pypi/simple`

## Anaconda安装
`Anaconda`是一个开源的`Python`发行版本，其包含了`conda`、`Python`等180多个科学包及其依赖项。使用`Anaconda`可以通过创建多个独立的`Python`环境，避免用户的`Python`环境安装太多不同版本依赖导致冲突。

## 代码安装
`github`代码会跟随开发进度不断更新
```
git clone https://github.com/PaddlePaddle/PaddleX.git
cd PaddleX
git checkout develop
python setup.py install
```
## pycocotools安装问题
`PaddleX`依赖`pycocotools`包，如安装`pycocotools`失败，可参照如下方式安装`pycocotools`

### Windows系统
`Windows`安装时可能会提示`Microsoft Visual C++ 14.0 is required`，从而导致安装出错，下载`VC build tools`安装再执行如下`pip`命令
注意：安装完后，需要重新打开新的终端命令窗口
```
pip install cython
pip install git+https://gitee.com/jiangjiajun/philferriere-cocoapi.git#subdirectory=PythonAPI
```
### Linux/Mac系统
Linux/Mac系统下，直接使用pip安装如下两个依赖即可
```
pip install cython  
pip install pycocotools
```
# 安装OpenVINO环境
##  前言

本指南适用于 `Microsoft Windows* 10 64 位`。 有关 `Linux*` 操作系统信息和说明，请参阅 `Linux `[安装指南](https://docs.openvinotoolkit.org/latest/openvino_docs_install_guides_installing_openvino_linux.html)。

> 提示：您可以使用 `OpenVINO™` 深度学习工作台 (`DL Workbench`) 内的模型优化器快速入门。 `DL Workbench` 是一个 `OpenVINO™` 用户接口，可让您导入模型、分析其性能和准确性、可视化输出、优化和准备模型以在各种Intel® 平台上部署。

## 介绍

> 重要提示:
> - 除有特殊说明外，本指南中的所有步骤都必须执行
> - 除下载安装包以外,也必须安装依赖，完成所有的配置

完成以下所有步骤，即可完成安装：
1. 安装 `Intel® OpenVINO™` 核心工具组件
2. 安装依赖工具与软件
	- `Microsoft Visual Studio* 2019 with MSBuild`
	- `CMake 3.14 or higher 64-bit`
	- `Python 3.6 - 3.8 64-bit`
		

	> 重要提示: 作为安装流程中的一部分, 请确认在安装`Python`依赖时，勾选`Add Python 3.x to PATH`将`Python`安装路径添加到`PATH`环境变量中。

3. 设置环境变量
4. 配置模型优化器 (`Model Optimizer`)
5. 可选安装步骤: 
	- 安装`windows`版本`Intel® Graphics` 驱动
	- 使用 `Intel® Movidius™ VPU` 为`Intel® Vision Accelerator Design`(`intel`视觉加速器设计)安装驱动程序和软件
	- 更新 `Windows*` 环境变量(如果安装`Python`时没有勾选`add Python to the path` 则此步骤为必需项)
此外，本指南同样涵盖以下步骤：
- 代码示例和入门演示程序
- 卸载`OpenVINO™` 工具套装

## 关于 Intel  OpenVINO™ 工具包的介绍
`OpenVINO™` 工具包是一个全面的工具包，用于快速开发解决各种任务的应用程序和解决方案，包括模拟人类视觉、自动语音识别、自然语言处理、推荐系统等。 该工具包基于最新一代人工神经网络，包括卷积神经网络 (`CNN`)、循环网络和基于注意力的网络，可跨英特尔® 硬件扩展计算机视觉和非视觉工作负载，从而最大限度地提高性能。 它通过从边缘主机到云端部署的高性能、人工智能和深度学习推理来加速应用程序。

更多详细信息，请见[详情页](https://software.intel.com/en-us/OpenVINO-toolkit)


适用于` Windows* 10 `操作系统的`Intel® OpenVINO™` 工具套件发行版：

- 启用基于`CNN`的深度学习推理边缘计算
- 支持跨`Intel® CPU`、`Intel® GPU`、`Intel® Neural Compute Stick  2` 和`Intel® Vision Accelerator Design`与`Intel® Movidius™ VPU` 的异构执行
- 通过易于使用的计算机视觉功能库和预先优化的内核加快上市时间
- 包括对计算机视觉标准的优化调用，包括 `OpenCV*` 和 `OpenCL™`
 
 
本次安装默认包含以下组件

|  组件   |  描述  |
| ------------------------- | ------------------------ |
| Model Optimizer     |   该工具将在流行框架中训练的模型导入、转换和优化为英特尔工具（尤其是推理引擎）可用的格式。注意：流行的框架包括 Caffe*、TensorFlow*、MXNet* 和 ONNX* 等框架。|
 Inference Engine     |这是运行深度学习模型的引擎，包含一系列可轻松将推理整合到应用的依赖库。|
| OpenCV*                |	OpenCV* community version compiled for Intel® hardware |
| Inference Engine Samples |	一组简单的控制台应用程序，演示如何在应用程序中使用Intel的深度学习推理引擎。.|
| Demos                  |	一组控制台应用程序，演示如何在应用程序中使用推理引擎来解决特定用例|
| Additional Tools |	一组用于模型的工具，包括精度检查器实用程序、训练后优化工具指南、模型下载器等 |
| Documentation for Pre-Trained Models |	Open Model Zoo 存储库中提供的预训练模型的文档 |

## 系统要求
### 硬件要求

 - 第 6 代至第 11 代英特尔® 酷睿™ 处理器和英特尔® 至强® 处理器
 - 第三代英特尔® 至强® 可扩展处理器（原代号为 `Cooper Lake`）
 - 英特尔® 至强® 可扩展处理器（以前称为 `Skylake` 和 `Cascade Lake`）
 - 英特尔凌动® 处理器，支持英特尔® Streaming SIMD Extensions 4.1（英特尔® SSE4.1）
 - 英特尔奔腾® 处理器 N4200/5、N3350/5 或 N3450/5 与英特尔® 高清显卡
 - 英特尔® 锐炬® Xe MAX 显卡
 - 英特尔® 神经计算棒 2(`Neural Compute Stick 2`)
 - 采用Intel® Movidius™ VPU 的Intel® 视觉加速器设计(`Vision Accelerator Design`)

> 注: `OpenVINO™ 2020.4`不再支持 `Intel® Movidius™ Neural Compute Stick`.

> 关于处理器：
> - 并非所有处理器都包含处理器图形。 有关处理器的信息，请参阅处理器规格。[详细链接](https://ark.intel.com/content/www/us/en/ark.html#@Processors)
> - 如果您使用的是英特尔至强处理器，则需要支持处理器图形的芯片组。 有关您的芯片组的信息，请参阅芯片组规格。[详细信息](https://ark.intel.com/content/www/us/en/ark.html#@Chipsets)

### 操作系统
`Microsoft Windows* 10 64-bit` 

### 软件要求

 - `Microsoft Visual Studio* with C++ 2019 or 2017 with MSBuild` [下载链接](http://visualstudio.microsoft.com/downloads/)
 - `CMake 3.10 or higher 64-bit`
	> 注: 如果您需要使用 `Microsoft Visual Studio 2019`, 需要安装 `CMake 3.14`.[下载链接](https://cmake.org/download/)
- `Python 3.6 - 3.8 64-bit` [下载链接](https://www.python.org/downloads/windows/)

## 安装步骤

> 请确保您的硬件满足上述系统需求，软件依赖如 `Microsoft Vusual Studio` 和 `CMake `已安装

### 安装 Intel® of OpenVINO™ 工具包核心组件
 1. 如果您还没有下载 Intel® Distribution of OpenVINO™ 工具包, [点击此处下载](https://software.intel.com/content/www/us/en/develop/tools/openvino-toolkit/download.html).下载的安装包默认文件名为 `w_openvino_toolkit_p_<version>.exe`.  
   ![enter description here](./images/1626232559584.png)
 
> 推荐：从上到下依次选择操作系统、发行版本、软件版本、安装方式，建议选项分别为：`Windows`、`Web & Local 2021.3`、`Local`，即选择适用于`Windows`平台的`2021.3`版本的`本地安装包`

 2. 双击安装包，会弹出安装界面并让您选择安装路径，默认安装路径是` C:\Program Files (x86)\Intel\openvino_<version>`，为简化操作，会同时创建一个快捷方式指向这个安装目录` C:\Program Files (x86)\Intel\openvino_2021` ，如果您选择其他路径，同样会创建快捷方式
	> 注：如果在此前，您系统中已经安装了OpenVINO™ 工具，此次安装会使用已有的安装路径再次安装，如果您需要在其他路径安装此新版本，需要卸载原有的旧版本

 3. 点击`next`，选择是否允许软件收集与发送使用信息，随便选一个，再点击`next`
 4. 如果您缺少外部依赖项，您将看到一个警告屏幕。 写着您缺少的依赖项。 此时您无需采取其他措施。 安装 `Intel® Distribution of OpenVINO™` 工具套件核心组件后，再安装缺少的依赖项。 下面的截图表明您缺少两个依赖项(显示有三个警告，中间的GPU可忽略，两个缺少的依赖项应该是`Python`和`CMake`)：
 ![enter description here](./images/1626243781942.png)
5. 点击next，出现以下截图时，表示第一部分的安装已经完成。
   ![enter description here](./images/1626244345900.png)

### 安装依赖
如此前提到的关于MS Visual Studio和CMake已经安装，跳过此步骤到`配置环境变量`模块即可
1. 安装 `Microsoft Visual Studio* with C++ 2019 or 2017 with MSBuild` [下载链接](http://visualstudio.microsoft.com/downloads/)
2. 安装 `CMake 3.14`.[下载链接](https://cmake.org/download/)
 
### 配置环境变量

> 注: 如果您将OpenVINO 安装在非默认安装路径,在执行以下配置命令时将`C:\Program Files (x86)\Intel`替换您当前的安装路径。

您必须先更新多个环境变量，然后才能编译和运行 `OpenVINO`™ 应用程序。 打开命令提示符，并运行 `setupvars.bat`批处理文件来临时设置您的环境变量：
`C:\Program Files (x86)\Intel\openvino_2021\bin\setupvars.bat`
执行结果如下
```
C:\Users\aoto>C:\"Program Files (x86)"\Intel\openvino_2021\bin\setupvars.bat
Python 3.6.8
[setupvars.bat] OpenVINO environment initialized
```

> 重要提示: 不建议使用 Windows PowerShell* 运行这个配置脚本，推荐使用命令行工具。

环境变量已经设置好了，接下来配置`Model Optimizer`

 ### 配置`Model Optimizer`
 > 重要提示: 这些步骤是必需的。 您必须为至少一个框架配置模型优化器。 如果您不完成本节中的步骤，模型优化器将失败。
 1. Model Optimizer 说明
	模型优化器是英特尔® `OpenVINO` 工具套件发行版的关键组件。 如果不通过模型优化器运行模型，就无法对经过训练的模型进行推理。 当您通过模型优化器运行预训练模型时，您的输出是网络的中间表示 (IR)。 IR 是描述整个模型的一对文件：
	- .xml: 网络拓扑结构的描述
	- .bin: 含权重和偏差二进制数据

	推理引擎使用跨 `CPU`、`GPU `或 `VPU `硬件的`通用 API` 读取、加载和推断 `IR `文件。
	模型优化器是一个基于 `Python` 的命令行工具 (`mo.py`)，位于 `C:\Program Files (x86)\Intel\openvino_2021\deployment_tools\model_optimizer`。 在使用 `Caffe`、`TensorFlow`、`MXNet `和 `ONNX `等流行深度学习框架训练的模型上使用此工具，将它们转换为推理引擎可以使用的优化的 `IR` 格式。

	本节说明如何使用脚本同时为所有支持的框架或单个框架配置模型优化器。 如果您想手动配置模型优化器而不是使用脚本，请参阅配置模型优化器页面上的使用手动配置过程部分。

	有关模型优化器的更多信息，请参阅模型优化器开发人员指南。
	
  2. Model Optimizer 配置步骤

您可以一次为所有支持的框架或一次为一个框架配置模型优化器。 选择最适合您需求的选项。 如果您看到错误消息，请确保您安装了所有依赖项。

> 重要提示：需要访问 Internet 才能成功执行以下步骤。 如果您只能通过代理服务器访问 Internet，请确保在您的环境中已经正确配置。


> 请注意 ： 
> - 如果您想从已安装的`OpenVINO` 的另一个已安装版本中使用`模型优化器`，请将 `openvino_2021` 替换为 `openvino_<version>`，其中` <version>` 是所需的版本。
> - 如果您将`OpenVINO`安装到非默认安装目录，请将 `C:\Program Files (x86)\Intel` 替换为您安装该软件的目录。

以下步骤请使用命令行界面执行以确保再报错时可以看到错误信息：

选项一 
1. 打开命令行(cmd.exe)
2. 进入脚本目录 
`cd C:\Program Files (x86)\Intel\openvino_2021\deployment_tools\model_optimizer\install_prerequisites`
3. 执行脚本
`install_prerequisites.bat`

选项二 
1. 打开命令行
2. 进入脚本目录 `cd C:\Program Files (x86)\Intel\openvino_2021\deployment_tools\model_optimizer\install_prerequisites`
3. 分别为不同的框架运行不同的配置脚本，可运行多次(不同的脚本)
	  - Caffe框架
	`install_prerequisites_caffe.bat`
	  - TensorFlow 1.x
	    `install_prerequisites_tf.bat`
	  - TensorFlow 2.x
	    `install_prerequisites_tf2.bat`
	  - MXNet
	    `install_prerequisites_mxnet.bat`
	  - ONNX
	    `install_prerequisites_onnx.bat`
	  - Kaldi
	    `install_prerequisites_kaldi.bat`

以上两个安装选项任选其一即可，推荐使用选项一，执行次数少，方便快捷。

## OpenVINO工作流与Demo试运行

### OpenVINO 组件介绍

工具包由三个主要组件组成：

- `Model Optimizer`(模型优化器)：优化英特尔架构的模型，将模型转换为与推理引擎兼容的格式。此格式称为中间表示 （IR）。
- `Intermediate Representation`(简称 IR)：模型优化器输出。模型转换为已优化为英特尔架构的格式，可通过推理引擎使用。
- 推理引擎：针对 IR（优化模型）运行推理以生成推理结果的软件库。

此外，还提供演示脚本、代码示例和演示应用程序，以帮助您使用工具包启动和运行：

- 演示脚本 - 自动执行工作流步骤以显示不同场景的运行推理管道的批次脚本。
- 代码示例 - 显示如何：
	- 在应用程序中使用特定的 OpenVINO 功能。
	- 执行特定任务，如加载模型、运行推理、查询特定设备功能等。
- 演示应用程序 - 提供强大应用程序模板以帮助您实现特定深度学习场景的控制台应用程序。这些应用程序涉及越来越复杂的处理管道，这些管道从同时运行推理的多个模型中收集分析数据，例如在视频流中检测一个人，以及检测人的身体属性，如年龄、性别和情绪状态。

### OpenVINO 工作流
简化的OpenVINO工作流程是：

- 获取预训练模型，可执行如行人检测、人脸检测、车辆检测、车牌识别、头部姿势等推理任务
- 运行预训练模型，通过Model Optimizer,将模型转化为中间形式(Intermediate Representation，简称 IR),IR 包含一对作为推理引擎的输入之的.xml文件按和.bin文件
- 在应用程序中使用推理引擎 API 对 IR（优化模型）运行推理和输出推理结果。该应用程序可以是一个开放的OpenVINO示例，或您自己的应用程序。

### 运行demo
OpenVINO内置运行Demo脚本位于` <INSTALL_DIR>\deployment_tools\demo`,可以作为了解OpenVINO的工作流的简单示例。这些脚本自动执行工作流流程，针对不同场景，演示推理管道。主要演示的内容有：
 - 编译多个实例文件，这些示例文件来自于OpenVINO组件内置文件
 - 下载预训练模型
 - 按步骤执行并将结果显示在控制台

示例脚本可以运行在任意满足条件的设备上。默认使用CPU进行推理，可使用 -d 参数指定其他推理设备 如GPU，通用指令如下：
`.<script_name> -d [CPU, GPU, MYRIAD, HDDL]`

推理管道示例脚本
该demo_security_barrier_camera使用车辆识别，其中车辆属性相互建立，以缩小特定属性。

脚本主要内容:

- 下载三个预训练IR模型
- 生成安保摄像头演示应用程序
- 运行程序，使用下载的模型和示例图片演示推理流程

应用程序主要功能:

- 识别被标注为车辆的对象
- 使用车辆标识作为对第二个模型的输入，该模型可识别特定车辆属性，包括车牌。.
- 使用车牌照作为第三个模型的输入，该模型识别牌照上的文字与数字

执行脚本:
`.\demo_security_barrier_camera.bat`
脚本执行过程中会访问网络下载模型等依赖，等待脚本执行完成时，弹出图片识别窗口如下图：
![enter description here](./images/1626254074956.png)

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。