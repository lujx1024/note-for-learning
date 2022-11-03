---
title: CentOS使用yum安装高版本gcc
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---
# 问题
在某些应用场景中，需要高版本的gcc支持，编译gcc耗时耗力，这里介绍一种简便的方法。

# 解决方案
红帽官方`Developer Toolset`文档[地址](https://access.redhat.com/documentation/en-us/red_hat_developer_toolset/8/)
用红帽官方提供的开发工具包来管理`gcc`版本，可以做到多版本并存，随时切换，还不破坏原有`gcc`环境。

# `devtoolset`对应`gcc`的版本
`devtoolset-3`对应`gcc4.x.x`版本
`devtoolset-4`对应`gcc5.x.x`版本
`devtoolset-6`对应`gcc6.x.x`版本
`devtoolset-7`对应`gcc7.x.x`版本

# 安装
```
yum install centos-release-scl
yum install devtoolset-4
```

# 激活gcc版本
```
scl enable devtoolset-4 bash
或
source /opt/rh/devtoolset-4/enable
```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。