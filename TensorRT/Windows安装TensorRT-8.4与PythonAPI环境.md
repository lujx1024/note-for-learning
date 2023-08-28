[TOC]

# 概述

本文档记录一下在Windows环境下安装TensorRT-8.4.x，并在`python`虚拟环境中安装`API`的方法。

# 安装

## 前置环境

- Windows 10 
- Visual Studio 2019
- NVIDIA GeForce 2060 SUPER
- CUDA 11.0
- cuDNN 8.2.x
- python 3.8

上述环境请确保安装完成，Python版本是指虚拟环境中的版本，可使用`conda`或`venv`创建虚拟环境。直接使用宿主机环境的同学请随意.

## 解压安装

下载TensorRT-8.4.x的安装包，解压到指定目录，例如`D:\TensorRT-8.4.3.1`,解压后的目录结构如下：

```bash
D:\TensorRT-8.4.3.1
├─bin
├─data
├─doc
├─graphsurgeon
├─include
├─lib
├─onnx_surgeon
├─python
├─samples
└─uff
```

配置环境变量,添加`D:\TensorRT-8.4.3.1\bin`到`PATH`中。

## 安装Python API

1. 创建虚拟环境
   
   ```bash
   conda create -n trt python=3.8 -y
   conda activate trt
   ```
2. 安装`tensorrt-**.whl`

   ```bash
   pip intall D:\TensorRT-8.4.3.1\python\tensorrt-tensorrt-8.4.3.1-cp38-none-win_amd64.whl
   ```

3. 安装其他`whl`

   ```bash
    pip install D:\TensorRT-8.4.3.1\onnx_graphsurgeon\onnx_graphsurgeon-0.3.12-py2.py3-none-any.whl

    pip install D:\TensorRT-8.4.3.1\graphsurgeon\graphsurgeon-0.4.6-py2.py3-none-any.whl    

    pip install D:\TensorRT-8.4.3.1\uff\uff-0.6.9-py2.py3-none-any.whl
    ```

> 安装完成相应的库以后，需要注意将TensorRT-8.4.3.1文件夹下的lib\include中的文件进行如下拷贝工作，防止在运行tensorrt时候无法找到相对应的Nvinfer.dll
>  - TensorRT-8.4.3.1中include文件夹下所有文件拷贝到C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.6\include
> - TensorRT-8.4.3.1中lib文件夹下所有lib文件拷贝到C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.6\lib\x64
> - TensorRT-8.4.3.1中lib文件夹下所有dll文件拷贝到C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v11.6\bin



# 测试

## Python环境导入tensorrt

```python
E:\..\yolov5-6.1 yolo_cp38> python

Python 3.8.17 (default, Jul  5 2023, 20:44:21) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import tensorrt as trt
>>> trt.__version__
'8.4.3.1'
>>>
```

## 使用YOLOv5项目测试

部署YOLOv5项目，使用预训练模型导出engine文件，项目部署方式不再赘述，导出engine文件的方式如下：

```python
python export.py --weights yolov5s --include engine --device 0
```

