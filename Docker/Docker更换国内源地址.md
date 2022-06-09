---
title: Docker更换国内源地址
tags: Docker,换源
renderNumberedHeading: true
grammar_cjkRuby: true
---

1. 创建配置文件
```
mkdir /etc/docker

vim /etc/docker/daemon.json
```
2. 添加国内源,保存退出
```
{
	"registry-mirrors": [
	"https://docker.mirrors.ustc.edu.cn",
	"http://hub-mirror.c.163.com",
	"https://registry.docker-cn.com"
	]                                      
}
```
3. 重启docker

`systemctl restart docker`
4. 查看
```
# 查看docker信息
docker info

# 输出(省略部分)
Registry Mirrors:
  https://docker.mirrors.ustc.edu.cn/
  https://kfwkfulq.mirror.aliyuncs.com/
  https://2lqq34jg.mirror.aliyuncs.com/
  https://pee6w651.mirror.aliyuncs.com/
  https://registry.docker-cn.com/
  http://hub-mirror.c.163.com/
 Live Restore Enabled: false
```


欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。