---
title: opencv计算图片模糊程度
tags: Python,opencv,模糊程度
renderNumberedHeading: true
grammar_cjkRuby: true
---

## 概述
`opencv-python`提供了拉普拉斯算子的接口方法计算图片模糊程度，使用时需要注意一下关键点：

1. 表示模糊程度的数值大小与图片本身的大小相关，不同大小的图片需要`resize`同一尺寸后计算
2. 计算出来的数值越大，表示图片越清晰
3. 在没有相同尺寸的对比图片的情况下，需要通过现有的数据设置一个阈值，以超过该阈值为标准判断图片清晰与否


```bash
import cv2

# step 1. read the image via opencv
image_path = 'test.jpg'
image = cv2.imread(image_path)

# step 2. resize the image to a specific size
image_resized = cv2.resize(image, (50, 50))

# step 3. get the gray image
gray = cv2.cvtColor(image_resized, cv2.COLOR_BGR2GRAY)

# step 4. get the blur value
blur = cv2.Laplacian(gray, cv2.CV_64F).var()

# step 5. compare the blur value to the threshold to determin weather the image is blur
. . .

```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。