---
title: CentOS安装Anaconda以及虚拟环境的设置
tags: CentOS,Anaconda,虚拟环境
renderNumberedHeading: true
grammar_cjkRuby: true
---

# 概述
`Anaconda`指的是一个开源的`Python`发行版本，其包含了`conda`、`Python`等180多个科学包及其依赖项。因为包含了大量的科学包，`Anaconda `的下载文件比较大，如果只需要某些包，或者需要节省带宽或存储空间，也可以使用`Miniconda`这个较小的发行版（仅包含`conda`和 `Python`）.
`Anaconda `是跨平台的，有 `Windows`、`MacOS`、`Linux `版本

# 下载安装

1. 执行下面的命令将执行脚本获取到本地（文件名可能因为版本不同有所差异）：
	`wget https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh`

2. 执行`bash Anaconda3-5.3.1-Linux-x86_64.sh`进行`Anaconda`的安装

	进入安装程序，提示输入“ENTER”继续：
	```
	Please,press ENTER to continue
	>>> ENTER
	```

3. 输入yes确认接受许可协议
	```
	Do you accept the license terms? [yes|no]
	[no] >>> yes
	```

4. 确认Anaconda的安装位置, 可改可不改
	```
	Anaconda3 will now be installed into this location:
	/root/anaconda3
	  - Press ENTER to confirm the location
	  - Press CTRL-C to abort the installation
	  - Or specify a different location below

	[/root/anaconda3] >>> /opt/anaconda3
	```
	> 其实安装位置可以在执行安装脚本的时候直接指定
	> 像上面要指定安装到`/opt/anaconda3`目录下，可以这样修改执行内容：
	> `bash bash Anaconda3-5.3.1-Linux-x86_64.sh -p /opt/anaconda3`，
	> 这样这一步就可以直接回车了。

5. 安装完成后，出现询问是否在用户的.bashrc文件中初始化Anaconda3的相关内容。
	```
	Do you wish the installer to initialize Anaconda3
	by running conda init? [yes|no]
	[no] >>> yes
	```
6. 执行下：`source ~/.bashrc`，之后就可以正常使用了。
7. 补充说明：配置其他用户可用，将安装脚本添加到`.bashrc`文件中内容添加到`/etc/bashrc`中。内容大致是下面这个样子的， 然后执行 `source /etc/bashrc`
	```
	# added by Anaconda3 5.3.1 installer
	# >>> conda init >>>
	# !! Contents within this block are managed by 'conda init' !!
	__conda_setup="$(CONDA_REPORT_ERRORS=false '/opt/anaconda3/bin/conda' shell.bash hook 2> /dev/null)"
	if [ $? -eq 0 ]; then
		\eval "$__conda_setup"
	else
		if [ -f "/opt/anaconda3/etc/profile.d/conda.sh" ]; then
			. "/opt/anaconda3/etc/profile.d/conda.sh"
			CONDA_CHANGEPS1=false conda activate base
		else
			\export PATH="/opt/anaconda3/bin:$PATH"
		fi
	fi
	```

# 简单环境配置
## 设置镜像源
```
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/
conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/
conda config --append channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/fastai/
conda config --append channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/
conda config --append channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/
 
 
 或直接写文件: 
 channels:
  - defaults
show_channel_urls: true
default_channels:
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/r
  - https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/msys2
custom_channels:
  conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  msys2: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  bioconda: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  menpo: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  pytorch: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  simpleitk: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
  
# 搜索时显示通道地址
conda config --set show_channel_urls yes
```

## 设置安装时显示源url，不想就改为no
`conda config --set show_channel_urls yes`

## 取消自动激活基础环境

通过将`auto_activate_base`参数设置为`false`实现：
`conda config --set auto_activate_base false`
如果反悔了还是希望`base`一直留着的话通过以下语句来恢复
`conda config --set auto_activate_base true`

## 更换环境依赖包保存路径
直接修改`~/.condarc` ，添加如下配置:
```
envs_dirs:
  - /home/conda/envs
pkgs_dirs:
  - /home/conda/pkgs
```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。