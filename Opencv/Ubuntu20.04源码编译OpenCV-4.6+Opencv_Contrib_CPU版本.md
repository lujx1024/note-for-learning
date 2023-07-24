[TOC]

# 概述

本文档主要描述在`Ubuntu20.04`系统平台，如何从源码编译`OpenCV-4.6``,包含`Opencv_Contrib`模块和支持`CUDA`支持。文档主要内容分为：

- 第一阶段：源码下载
- 第二阶段：工具和依赖库安装
- 第三阶段：编译安装
- 第四阶段：`c++`和`python`工具的验证测试
- 报错信息与解决方案
- 参考链接与参考文档

# 第一阶段：源码下载

本文档选择的是`OpenCV-4.6`版本，下载地址为：[OpenCV-4.6](https://github.com/opencv/opencv/archive/refs/tags/4.6.0.tar.gz)。下载完成后，解压到`opencv-4.6.0`文件夹。

同样,`Opencv_Contrib`模块的下载地址为：[Opencv_Contrib-4.6](https://github.com/opencv/opencv_contrib/archive/refs/tags/4.6.0.tar.gz)，下载完成后，解压到`opencv_contrib-4.6.0`文件夹。

为避免编译时出现错误，OpenCV和OpenCV_Contrib的版本**一定要一致**。

下载完成后，创建一个新的文件夹,可命名为`opencv_install`,将`opencv_contrib-4.6.0`和`opencv-4.6.0`放到此文件夹下，此时文件夹结构如下：

```bash
opencv_install
├── opencv-4.6.0
└── opencv_contrib-4.6.0
```

> 注：如需下载其他版本的OpenCV，可参考[OpenCV Releases](https://github.com/opencv/opencv/tags) 和 [OpenCV_Contrib Releases](https://github.com/opencv/opencv_contrib/tags),选择对应版本的源码下载。

# 第二阶段：工具和依赖库安装

```bash
sudo apt upgrade -y && sudo apt update -y

sudo apt install -y cmake g++ wget unzip

sudo apt-get install -y build-essential \
libgtk2.0-dev libavcodec-dev libavformat-dev \
libjpeg-dev libswscale-dev libtiff5-dev libpng-dev \
libtiff-dev libv4l-dev libxvidcore-dev libx264-dev \
libgtk-3-dev libblas-dev liblapack-dev gfortran python3-dev libgtk2.0-dev libavcodec-dev libjpeg-dev 
```

> 注 ： 确保`libgtk2.0-dev`正确安装，否则编译完成后的测试阶段会报错，强烈建议单独执行一次`apt install -y libgtk2.0-dev`

# 第三阶段：编译安装

## 3.0 修改依赖包下载链接

由于国内网络环境的原因，下载依赖包时需要访问`https://raw.githubusercontent.com`开头的地址，大概率会出现下载失败的情况，这里我们可以通过添加代理链接头`https://ghproxy.com/`的方式来解决这个问题。

```
原链接：
https://raw.githubusercontent.com/opencv/opencv_3rdparty/.../ippicv/
加代理的链接:
https://ghproxy.com/https://raw.githubusercontent.com/opencv/opencv_3rdparty/.../ippicv/
```

需要修改的文件有：

- opencv-4.6.0/3rdparty/ippicv/ippicv.cmake
- opencv-4.6.0/3rdparty/ffmpeg/ffmpeg.cmake

通过文本编辑器打开上述文件，将原链接替换为代理链接即可。

## 3.1 创建编译目录

```bash
cd opencv_install/opencv-4.6.0
mkdir build
cd build
```

## 3.2 (可选)创建Python虚拟环境

1. 下载安装包

    ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda3-py311_23.5.2-0-Linux-x86_64.sh
    ```

2. 安装

    ```bash
    bash Miniconda3-py311_23.5.2-0-Linux-x86_64.sh
    ```

## 3.3 编译安装

修改配置项,提到的配置项都是必须修改的，其他配置项可根据需求自行修改。

> 注: 配置项中，所有涉及到路径的，一律使用绝对路径。例如家目录`~`，需要写成`/root/`或其他用户的家目录绝对路径，例如`/home/ubuntu/`。


```bash
cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D INSTALL_C_EXAMPLES=OFF \
    -D OPENCV_ENABLE_NONFREE=ON \
    -D OPENCV_EXTRA_MODULES_PATH=/opencv_contrib-4.6.0/modules/ \
    -D BUILD_TESTS=OFF \
    -D BUILD_opencv_wechat_qrcode=OFF \
    -D BUILD_opencv_xfeatures2d=OFF \
    -D BUILD_opencv_face=OFF \
    -D OPENCV_GENERATE_PKGCONFIG=ON \
    ..
```

由于上述指令较长，可以将其保存为脚本文件`build_opencv.sh`，添加脚本执行权限，然后执行脚本文件即可。

> 注：先别着急执行，请先完成配置项的修改。


```bash
touch build_opencv.sh
vim build_opencv.sh # 将上述指令复制到脚本文件中
```

> 注：shell脚本文件中的`..`表示上一级目录，即`opencv-4.6.0`目录。

> 注：反斜杠`\`表示换行，后面不能有`空格`或`Tab`，否则执行脚本会报错。
```bash
chmod +x build_opencv.sh
./build_opencv.sh
```

`cmake` 完成后，执行编译安装指令，编译时间较长，请耐心等待：

```bash
make -j8
make install 
```
`make install`指令会把编译后的头文件和库写入到指定文件夹中，包括系统文件夹`/usr/local/bin`和`PYTHON`虚拟环境中

> 注：`-j8`表示使用8个线程进行编译，可以根据自己的CPU核心数进行调整。查询线程数指令：`nproc`，因此可使用`-j$(nproc)`.

## 3.4 配置环境变量

创建 `/etc/ld.so.conf.d/opencv.conf` 文件，添加OpenCV库文件路径：

```bash
vim /etc/ld.so.conf.d/opencv.conf
/usr/local/lib
```

执行指令:

```bash
ldconfig
```

修改环境变量`.bashrc`
```
vim ~/.bashrc
```

```bash
#opencv4.2.0环境变量
export PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/lib/pkgconfig
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib
```

执行source命令使环境变量生效

```bash
source ~/.bashrc
```

因为，对于OpenCV4以上的版本要使用OpenCV4才能正确查询到其版本，库以及头文件目录的值。具体命令如下所示：

```bash
pkg-config --modversion opencv4
pkg-config --cflags opencv4
pkg-config --libs   opencv4
```

# 第四阶段：测试OpenCV

1. 创建测试文件夹`testopencv`,并进入该文件夹

    ```bash
    mkdir testopencv
    cd testopencv
    ```

2. 创建测试文件`main.cpp`,并编写测试代码

    ```bash
    # include <iostream>
    # include <opencv2/opencv.hpp>
    using namespace std;
    using namespace cv;
    int main(){
        Mat img=imread("dog.jpg");
        imshow("test", img);
        waitKey(0);
        return 0;
    }
    ```

3. 编写CMakelists.txt文件

    ```bash
    cmake_minimum_required(VERSION 3.0)
    project(testopencv)
    
    # c++ 11
    set(CMAKE_CXX_FLAGS "-std=c++11")
    find_package(OpenCV REQUIRED)
    include_directories(OpenCV_INCLUDE_DIRS) # load opencv header files
    add_executable(testopencv main.cpp) # create exe file
    target_link_libraries(testopencv ${OpenCV_LIBS}) # link llib files to exe    
    ```

4. 执行编译指令

    ```bash
    mkdir build
    cd build
    cmake ..
    make
    ```

5. 执行测试指令

    ```bash
    ./testopencv
    ```

    > 注：确保build文件夹中存在`dog.jpg`文件

# 报错与解决方案

1. `imshow`报错

    ```bash
    (testopencv:1): Gtk-WARNING **: 14:50:57.000: cannot open display: 
    ```

    > 解决方案：在`CMakeLists.txt`文件中添加`set(OpenCV_DIR /usr/local/share/OpenCV)`，并重新编译。

2. cuDNN软连接失效
   由于配置CUDA和cuDNN过程中，直接复制cuDNN文件到CUDA安装目录会导致软连接失效，因此需要重新配置cuDNN，具体步骤如下：

   ```bash
    # 进入cuDNN安装目录
    cd /usr/local/cuda-11.2/targets/x86_64-linux/lib
    # 手动创建软连接
    ln -sf libcudnn_cnn_infer.so.8.4.0 libcudnn_cnn_infer.so.8
    ln -sf libcudnn_cnn_infer.so.8 libcudnn_cnn_infer.so
    ln -sf libcudnn.so.8.4.0 libcudnn.so.8
    ln -sf libcudnn.so.8 libcudnn.so
    ln -sf libcudnn_ops_infer.so.8.4.0 libcudnn_ops_infer.so.8
    ln -sf libcudnn_ops_infer.so.8 libcudnn_ops_infer.so
    ln -sf libcudnn_adv_infer.so.8.4.0 libcudnn_adv_infer.so.8
    ln -sf libcudnn_adv_infer.so.8 libcudnn_adv_infer.so
    ln -sf libcudnn_cnn_train.so.8.4.0 libcudnn_cnn_train.so.8
    ln -sf libcudnn_cnn_train.so.8 libcudnn_cnn_train.so
    ln -sf libcudnn_adv_train.so.8.4.0 libcudnn_adv_train.so.8
    ln -sf libcudnn_adv_train.so.8 libcudnn_adv_train.so
    ln -sf libcudnn_ops_train.so.8.4.0 libcudnn_ops_train.so.8
    ln -sf libcudnn_ops_train.so.8 libcudnn_ops_train.so
   
    # 下面是另一种方法
    tar -xzvf cudnn-11.4-linux-x64-v8.2.4.15.tgz
    sudo cp cuda/include/cudnn*.h /usr/local/cuda/include
    sudo cp cuda/lib64/libcudnn* /usr/local/cuda/lib64
    sudo chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn*
    sudo ldconfig
   ```

# 参考资料

1. [OpenCV官网](https://docs.opencv.org/4.8.0/d7/d9f/tutorial_linux_install.html)
2. [CSDN](https://blog.csdn.net/u013454780/article/details/128357962)
3. [CSDN](https://blog.csdn.net/ChunjieShan/article/details/125391238)
4. [CSDN](https://blog.csdn.net/luoluonuoyasuolong/article/details/80409644)