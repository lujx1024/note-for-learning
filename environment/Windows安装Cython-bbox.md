---
title: Windows安装Cython-bbox
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---

1. 下载源码文件[下载链接](https://pypi.org/project/cython-bbox/#files)

2. 在目录中使用文本打开`setup.py`，找到第31行，把其中`extra_compile_args=[’-Wno-cpp’]`的替换`为extra_compile_args={'gcc': ['/Qstd=c99']}`

3.` python setup.py build_ext install`

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。