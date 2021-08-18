---
title: PaddleDetection多卡训练与NCCL安装
tags: PaddleDetection,多GPU训练,NCCL
renderNumberedHeading: true
grammar_cjkRuby: true
---
# 查看已安装NCCL
几种查询已安装NCCL的方法
1. `whereis nccl`
	`nccl: /usr/include/nccl.h`
	
2. `find / -name libnccl*`
	```
	/var/nccl-repo-2.8.3-ga-cuda10.1/libnccl-2.8.3-1+cuda10.1.x86_64.rpm
	/var/nccl-repo-2.8.3-ga-cuda10.1/libnccl-devel-2.8.3-1+cuda10.1.x86_64.rpm
	/var/nccl-repo-2.8.3-ga-cuda10.1/libnccl-static-2.8.3-1+cuda10.1.x86_64.rpm
	/usr/lib64/libnccl.so.2
	/usr/lib64/libnccl.so
	/usr/lib64/libnccl.so.2.8.3
	/usr/lib64/libnccl_static.a
	/usr/share/doc/libnccl-2.8.3
	/usr/share/doc/libnccl-devel-2.8.3
	/usr/share/doc/libnccl-static-2.8.3
	```
3. `rpm -qa | grep nccl`
	```
	libnccl-static-2.8.3-1+cuda10.1.x86_64
	nccl-repo-rhel7-2.8.3-ga-cuda10.1-1-1.x86_64
	libnccl-devel-2.8.3-1+cuda10.1.x86_64
	libnccl-2.8.3-1+cuda10.1.x86_64
	```
4. `yum list installed | grep nccl`

	```
	libnccl.x86_64         2.8.3-1+cuda10.1   @nccl-2.8.3-ga-cuda10.1
	libnccl-devel.x86_64    2.8.3-1+cuda10.1  @nccl-2.8.3-ga-cuda10.1
	libnccl-static.x86_64   2.8.3-1+cuda10.1  @nccl-2.8.3-ga-cuda10.1
	```

# 卸载旧版本

## 使用RPM卸载
 此方法适用于使用以`.rpm`为扩展名的安装包安装的依赖库：
 
  - 首先检查已安装的依赖库的包名
	```
	[root@centos_aoto home]# rpm -qa | grep nccl
	libnccl-2.9.9-1+cuda11.3.x86_64
	libnccl-static-2.9.9-1+cuda11.3.x86_64
	libnccl-devel-2.9.9-1+cuda11.3.x86_64	
	```

- 卸载所有列出的包名
	```
	[root@centos_aoto home]# rpm -e libnccl-devel-2.9.9-1+cuda11.3.x86_64
	/sbin/ldconfig: /usr/local/cuda-10.1/targets/x86_64-linux/lib/libcudnn.so.7 is not a symbolic link

	[root@centos_aoto home]# rpm -e libnccl-2.9.9-1+cuda11.3.x86_64
	/sbin/ldconfig: /usr/local/cuda-10.1/targets/x86_64-linux/lib/libcudnn.so.7 is not a symbolic link

	[root@centos_aoto home]# rpm -e libnccl-static-2.9.9-1+cuda11.3.x86_64
	```

## 使用`yum` 卸载
- 查询已安装的依赖库的包名
	```
	(detection_head) [root@centos_aoto nccl-tests]# yum list installed | grep nccl
	libnccl.x86_64            2.8.3-1+cuda10.1      @nccl-2.8.3-ga-cuda10.1
	libnccl-devel.x86_64      2.8.3-1+cuda10.1      @nccl-2.8.3-ga-cuda10.1
	libnccl-static.x86_64     2.8.3-1+cuda10.1      @nccl-2.8.3-ga-cuda10.1
	nccl-repo-rhel7-2.8.3-ga-cuda10.1.x86_64    1-1    installed
	```

- 卸载已安装的依赖(待验证)

```
yum  erase <package_name>
```

# 安装适配版本
## 下载安装包

登录NVIDIA NCCL[官方网站](https://developer.nvidia.com/nccl/nccl-legacy-downloads)，下载对应本地环境中CUDA版本的NCCL本地安装包，本实例中，安装包名称为`nccl-repo-rhel7-2.8.3-ga-cuda10.1-1-1.x86_64.rpm`

## 安装依赖与安装包

1. 安装本地库
	`sudo rpm -i nccl-repo-<version>.rpm`
2. 更新`yum`源
	`sudo yum update`

3. 安装 NCCL
	`sudo yum install libnccl libnccl-devel libnccl-static`


# 测试NCCL环境
NVIDIA官方有一个测试NCCL环境的工具`nccl_tests`,[官方链接](https://github.com/NVIDIA/nccl-tests)

## nccl_tests 的安装与使用

1. 下载源代码
	 `https://github.com/NVIDIA/nccl-tests.git`
2. 编译
编译`nccl-tests`直接使用 `make`.指令即可
注 ：如果 CUDA 不是安装在 `/usr/local/cuda` 路径,则需要指定参数 `CUDA_HOME`. 同样, 如果 NCCL不是安装在 `/usr`, 同样需要指定 `NCCL_HOME`.

	```
	make CUDA_HOME=/path/to/cuda NCCL_HOME=/path/to/nccl
	```

3. 测试

	```
	## 测试 4 个 GPU (-g 4), 扫描范围从 8 Bytes 到 128MBytes
	./build/all_reduce_perf -b 8 -e 128M -f 2 -g 4
	```

> 参考链接 :
> 1. [PaddleDetection issue #3973](https://github.com/PaddlePaddle/PaddleDetection/issues/3973)
> 2. [NVIDIA NCCL issue #554](https://github.com/NVIDIA/nccl/issues/554)
> 3. [NCCL official installation guide](https://docs.nvidia.com/deeplearning/nccl/install-guide/index.html#rhel_centos)
> 4. [nccl-tests official github](https://github.com/NVIDIA/nccl-tests)


欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。