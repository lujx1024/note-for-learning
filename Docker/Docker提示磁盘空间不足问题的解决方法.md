---
title: Docker提示磁盘空间不足问题的解决方法
tags: Docker,Home Root Dir,Device Space
renderNumberedHeading: true
grammar_cjkRuby: true
---

[toc]

# 概述
在Docker使用的过程中，时常需要清理磁盘，下载新的镜像运行，但是当现有的硬盘没有足够的存储空间最终运行依然会报错==磁盘空间不足 #E91E63==.
这里记录一下几种解决docker使用时的磁盘空间不足的问题

# 解决方法
## prune指令
### `docker system prune`
首先想到使用`prune`指令删除当前的未使用的容器
`docker system prune`
> 注: `docker system prune` 可添加不同的参数完成不同的操作,执行指令前需确认相关参数是否正确


执行这条指令时需要留心，因为此指令在以下几种的情况下，会删除所有的文件：

- 所有未启动的容器  
- 所有未被任何一个容器使用的网络
-  所有虚悬镜像
-  所有虚悬构建缓存

所以，在执行指令前，确保需要保留的容器，不在上述几个分类中。
```
WARNING! This will remove:
  - all stopped containers
  - all networks not used by at least one container
  - all dangling images
  - all dangling build cache

Are you sure you want to continue? [y/N]
```
输入`Y`, 继续执行删除操作。

 ### `docker system prune –volumes`
 `docker system prune`可以删除镜像(`image`)、容器(`container`)和网络(`network`)，但是无法删除数据卷(`volume`). 可以加入 `--volumes` 参数用来删除数据卷(`volume`).

```
docker system prune --volumes
```

如果想同时删除镜像(`image`)、容器(`container`)和网络(`network`)以及关联的数据卷(volume),可以使用`--all`参数
```
docker system prune –all
```
## 删除所有的孤立卷(`orphaned volumes`)
第二种方法是删除当前docker中的所有孤立卷(`orphaned volumes`)，在执行删除操作之前，可使用listiling指令查看当前的所有孤立卷(`orphaned volumes`)，指令如下
```
# 查询
docker volume ls -qf dangling=true
#删除
docker volume rm $(docker volume ls -qf dangling=true)
```
## 删除未使用的镜像(images)
在执行这一步之前，强烈建议检查一下系统中是否有可删除的未使用volume，并执行上述中的第二步操作，删除所有的孤立卷(`orphaned volumes`).
假设上述所有的操作已经执行，按照下面的指令删除未使用的镜像：
```
# 查询当前所有镜像
docker image ls 

# 根据镜像名称筛选需要删除的镜像
docker rmi $(docker images | grep `<image_name>` | awk '{print $3}')
# 或执行
docker rmi {image-name}
```
## 更换默认主目录(`Root Dir`)
如果上述步骤仍然没有解决问题，可以尝试更改Docker默认的保存地址，即主目录(`Docker Home Root Dir`)地址,Docker默认保存地址是`/var/lib/docker`,现在，需要将改地址更换到其他空间较大的目录。

- step 1  创建新的Docker根目录
	```
	mkdir -p /home/docker/lib
	```
- step 2 停止docker服务
	```
	# 停止所有容器
	docker stop $(docker ps -aq)
	# 停止docker系统服务
	systemctl stop docker
	```

- step 3 迁移现有的docker文件到新文件路径

	```
	rsync -avz /var/lib/docker /home/docker/lib
	```
-  step 3 修改 /etc/docker/daemon.json ,添加以下配置
	```
	{
		"graph":"/docker/lib/docker"
	}

	```
- step 4 重新加载配置，重启docker服务

	```
	# 重载配置
	systemctl daemon-reload 
	# 重新启动服务
	systemctl restart docker

	```
- step 5 确认信息

	```
	docker info

	# 输出如下(删除部分信息)， Docker Root Dir 已更换
	Client:
	 Context:    default
	 Debug Mode: false
	 Plugins:
	  app: Docker App (Docker Inc., v0.9.1-beta3)
	  buildx: Docker Buildx (Docker Inc., v0.8.2-docker)
	  scan: Docker Scan (Docker Inc., v0.17.0)

	Server:
	 Containers: 1
	  Running: 1
	  Paused: 0
	  Stopped: 0
	 Images: 12
	 Server Version: 20.10.16
	  ...
	 OSType: linux
	 Architecture: x86_64
	 CPUs: 48
	 Total Memory: 251.8GiB
	 Name: localhost.localdomain
	 ID: B443:ILBW:QET7:KPO4:K5YK:RRTC:YTTE:W4AS:N2YR:W6EM:QL3U:5IMX
	 Docker Root Dir: /home/docker/lib/docker
	 Debug Mode: false
	 Registry Mirrors:
	  https://docker.mirrors.ustc.edu.cn/
	  https://registry.docker-cn.com/
	 Live Restore Enabled: false

	```
## 另一种更换主目录的方法(仅供参考)

```
# 1.创建新目录
mkdir /app/sample_direction/my_local_storage
# 2.更改权限
chmod -R 777 /app/sample_direction/my_local_storage
# 3.更新docker服务配置
vi /usr/lib/systemd/system/docker.service 

# 添加或更改以下配置
ExecStart=/usr/bin/dockerd -s devicemapper --storage-opt dm.fs=xfs --storage-opt dm.basesize=40GB -g /app/sample_direction/my_local_storage --exec-opt native.cgroupdriver=cgroupfs

注: 如果设备类型是 overlay2 需要添加 add -g /apps/newdocker/docker 到服务配置中

# 4.删除原目录
rm -rf /var/lib/docker 
# 5. 关闭docker服务
systemctl stop docker 
# 6. 重装配置
systemctl daemon-reload 
# 7. 启动服务
systemctl start docker

```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。