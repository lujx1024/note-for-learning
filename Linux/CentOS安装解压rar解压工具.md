---
title: CentOS安装解压rar解压工具
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---

1. 下载安装包
	```
	wget https://www.rarlab.com/rar/rarlinux-x64-612.tar.gz
	```
2. 解压编译
	```
	tar xzvf rarlinux-x64-612.tar.gz
	cd rar
	make
	```

3. 使用
	```
	rar x something.rar
	```


欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。