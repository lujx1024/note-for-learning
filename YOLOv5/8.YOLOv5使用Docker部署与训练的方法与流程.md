[TOC]

# 概述

本文档主要讲述YOLOv5使用Docker部署与训练的方法与流程。

# 部署方法

## 先决条件

- 操作系统: `Linux`发行版，推荐使用`Ubuntu 20.04`
- `GPU`驱动: 已安装最新的`NVIDIA`驱动，驱动下载地址:[Driver](https://www.nvidia.com/Download/index.aspx)
- 安装Docker: [Install Docker Engine on Ubuntu](https://docs.docker.com/engine/install/ubuntu/)
- 安装`nvidia-docker` [安装教程](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

> 注：上述所有的先决条件中，所有项目均需要满足且通过测试，否则后续部署中可能会导致问题。

## 获取YOLOv5镜像

`YOLOv5`官方镜像仓库地址：[ultralytics/yolov5](https://hub.docker.com/r/ultralytics/yolov5)，可以通过`docker pull`命令，针对不同的版本或架构需求，获取不同TAG的镜像。此处以`YOLOv5 v6.1 x86 GPU`版本为例，获取镜像的命令如下：

```bash
docker pull ultralytics/yolov5:v6.1
```

## 启动YOLOv5容器

1. 基础容器启动命令

   ```bash
   sudo docker run --ipc=host -it ultralytics/yolov5:v6.1
   ```

   > 注：上述命令启动了一个最基础的可交互YOLOv5容器

2. 可访问本地文件容器启动命令

   ```bash
   sudo docker run --ipc=host -it --gpus all -v "$(pwd)"/datasets:/usr/src/datasets --name yolov5 ultralytics/yolov5:v6.1
   ```

   > 注：上述命令启动了一个可访问本地文件的YOLOv5容器，其中`"$(pwd)"/datasets`为本地文件路径，`/usr/src/datasets`为容器内文件路径，两者可以不同，但是需要保证本地文件路径存在。

3. 指定GPU容器启动命令

    使用`--gpus`参数指定GPU，`--gpus all`表示使用所有GPU，`--gpus 0`表示使用GPU0，`--gpus 0,1`表示使用GPU0和GPU1，以此类推。

   ```bash
    sudo docker run --ipc=host -it --gpus all ultralytics/yolov5:v6.1
   ```

## 容器内部操作

上述操作完成后，即可进入容器内部，进行YOLOv5的训练、推理等操作。

# 模型训练

## 训练数据准备

YOLOv5数据集格式要求如下：

```bash
├── data
│   ├── train
│   │   ├── images
│   │   │   ├── 1.jpg
│   │   ├── labels
│   │   │   ├── 1.txt
│   ├── val
│   │   ├── images
│   │   │   ├── 2.jpg
│   │   ├── labels
│   │   │   ├── 2.txt

```

将数据集整理为上述格式后,保存在本地文件夹中，例如`/home/datasets/`文件夹，然后将本地文件夹挂载到容器内部，即可在容器内部访问本地文件夹中的数据集。

```bash
sudo docker run --ipc=host -it -v /home/datasets/:/usr/src/datasets ultralytics/yolov5:v6.1
```

此时，在容器中，YOLOv5项目源代码位于`/usr/src/app`,数据集位于`/usr/src/datasets`。

修改相应的配置文件，例如`/usr/src/app/yolov5/data/coco128.yaml`，将`train`和`val`的路径修改为`/usr/src/datasets/train`和`/usr/src/datasets/val`。

上述一应流程完成后，即可开始训练。训练方法与本地化安装相同，可选择单卡训练或多卡训练。
> 注: 是否使用多卡训练，取决于容器内部是否有多张GPU，如果容器内部有多张GPU，可以使用多卡训练，否则只能使用单卡训练。

## 模型的输出

模型训练完成后，模型的输出位于`/usr/src/app/runs/train/exp`，其中`exp`为默认的模型保存位置，此时的模型保存在容器之外，一旦容器被删除，模型也会被删除，因此，需要将模型保存到容器外部，可以通过`docker cp`命令将模型从容器内部拷贝到容器外部。

```bash
# 切换到容器外部执行指令
docker cp <容器ID>:/usr/src/app/runs/train/exp /home/models
```


# 参考链接

- [YOLOv5官方文档](https://docs.ultralytics.com/yolov5/environments/docker_image_quickstart_tutorial/)
- [YOLOv5官方镜像仓库](https://hub.docker.com/r/ultralytics/yolov5)

