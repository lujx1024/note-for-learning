---
title: dlib实现人脸关键点检测检测方法 
tags: dlib,landmark,Python
renderNumberedHeading: true
grammar_cjkRuby: true
---

[toc]
# 概述
dlib支持检测人脸特征关键点，官方提供了68维度和5维度的人脸关键店检测预训练模型提供下载使用。

# 关键点检测实现方法

## 实现步骤
1. 加载图片，进行人脸区域的检测 (包含人脸检测模型创建等)
2. 传入图片和人脸检测结果，获取人脸换关键点数据(包含face landmark模型创建等)
3. 解析人脸关键点数据

相关数据与模型文件下载：[地址](http://dlib.net/files/)
CNN人脸检测模型名称 ：`mmod_human_face_detector.dat.bz2`
68维人脸检测模型名称 ：  `shape_predictor_68_face_landmarks.dat.bz2`      
5维人脸检测模型名称  ：`shape_predictor_5_face_landmarks.dat.bz2`

## 代码示例

本实例中，使用CNN人脸检测模型和68维人脸关键点检测模型
```
import dlib
import numpy as np

from cv2 import cv2

# step 1. create the face detector and shape predictor model
face_detector_model_path = '../models/mmod_human_face_detector.dat'
face_detector = dlib.cnn_face_detection_model_v1(face_detector_model_path)  # dlib.cnn_face_detection_model_v1
shape_model_path = r'../models/shape_predictor_68_face_landmarks.dat'
face_shape_predictor = dlib.shape_predictor(shape_model_path)  # dlib.shape_predictor

# step 2. process face detection
# note that the difference between the image data formated as numpy.ndarray read by dlib and cv2 is that dlib read it channels as *R G B* order while cv2 read as *B G R*,so you should do one more step to convert the image if using cv2
image_path = "sample.jpg"
img = dlib.load_rgb_image(image_path)
# img = cv2.cvtColor(cv2.imread(image_path),cv2.COLOR_BGR2RGB)
detections = face_detector(img, 1)  # dlib.mmod_rectangles

# step 3. get shape of one face for example
detection = detections[0]  # dlib.mmod_rectangle
# the mmod_rectangle contains two parts : confidence and rect

shape = face_shape_predictor(img, detection.rect)  # dlib.full_object_detection

step 4. get all the face landmark points
 landmark_points = shape.parts() # dlib.points
```
## 效果实例
将所有的68维度人脸特征关键点连接之后的效果图如下所示

![landmark 68 sample](./images/1647569893863.png)

关键点的顺序与对应面部位置：
![enter description here](./images/6982eb7601e1d374594b26e0f0beba1.png)


# 关键类与接口方法

## 概述

1. 人脸检测类 :  `dlib.fhog_object_detector`和 `dlib.cnn_face_detection_model_v1`,前者基于HOG模型，后者基于CNN模型，前者检测方法调用为`__call(img)__ ->dlib.rectangles`和`run(img,upsample_num,threshold)->(dlib.rectangles,List[scores:int],List[int])`,后者检测方法调用为`__call(img)__->dlib.mmod_rectangles`
2. 关键点检测类: `dlib.shape_predictor`,预测调用方法`__call__(self,image, box: dlib.rectangle)->dlib.full_object_detection`
3. 检测结果类 : `dlib.full_object_detection`， 常用方法 `part(self, idx: int)->dlib.point` 单个关键点信息 、`parts(self)->dlib.points` 所有的关键点信息
4. 关键点类：`dlib.point`关键点，成员包含x，y，`dlib.points`关键点列表

## 关键点检测类: `dlib.shape_predictor`
```
class dlib.shape_predictor
    This object is a tool that takes in an image region containing some object and outputs a set of point locations that define the pose of the object. The classic example of this is human face pose prediction, where you take an image of a human face as input and are expected to identify the locations of important facial landmarks such as the corners of the mouth and eyes, tip of the nose, and so forth.

    __call__(self: dlib.shape_predictor, image: array, box: dlib.rectangle) → dlib.full_object_detection
        requires
            image is a numpy ndarray containing either an 8bit grayscale or RGB image.
            box is the bounding box to begin the shape prediction inside.
        ensures
            This function runs the shape predictor on the input image and returns a single full_object_detection.
    __init__(*args, **kwargs)
        Overloaded function.

    __init__(self: dlib.shape_predictor) -> None
    __init__(self: dlib.shape_predictor, arg0: unicode) -> None
        Loads a shape_predictor from a file that contains the output of the train_shape_predictor() routine.

    save(self: dlib.shape_predictor, predictor_output_filename: unicode) → None
    Save a shape_predictor to the provided path.
```
## 检测结果类 : `dlib.full_object_detection`

```
class dlib.full_object_detection
    This object represents the location of an object in an image along with the positions of each of its constituent parts.

    __init__(self: dlib.full_object_detection, rect: dlib.rectangle, parts: object) → None
        requires
            rect: dlib rectangle
            parts: list of dlib.point, or a dlib.points object.
    num_parts
        The number of parts of the object.
    
    part(self: dlib.full_object_detection, idx: int) → dlib.point
        A single part of the object as a dlib point.
    
    parts(self: dlib.full_object_detection) → dlib.points
        A vector of dlib points representing all of the parts.
    
    rect
        Bounding box from the underlying detector. Parts can be outside box if appropriate.
```
##  关键点类：`dlib.point`  `dlib.points`

```
class dlib.point
    This object represents a single point of integer coordinates that maps directly to a dlib::point.
    
    __init__(*args, **kwargs)
        Overloaded function.
    
    __init__(self: dlib.point, x: int, y: int) -> None
    __init__(self: dlib.point, p: dlib::vector<double, 2l>) -> None
    __init__(self: dlib.point, v: numpy.ndarray[int64]) -> None
    __init__(self: dlib.point, v: numpy.ndarray[float32]) -> None
    __init__(self: dlib.point, v: numpy.ndarray[float64]) -> None
    normalize(self: dlib.point) → dlib::vector<double, 2l>
        Returns a unit normalized copy of this vector.
    
    x
        The x-coordinate of the point.
    y
        The y-coordinate of the point.
```

```
class dlib.points
    An array of point objects.

    __init__(*args, **kwargs)
        Overloaded function.

    __init__(self: dlib.points) -> None
    __init__(self: dlib.points, arg0: dlib.points) -> None
        Copy constructor

    __init__(self: dlib.points, arg0: iterable) -> None
    __init__(self: dlib.points, initial_size: int) -> None
    append(self: dlib.points, x: dlib.point) → None
        Add an item to the end of the list

    clear(self: dlib.points) → None
    count(self: dlib.points, x: dlib.point) → int
        Return the number of times x appears in the list

    extend(*args, **kwargs)
        Overloaded function.

    extend(self: dlib.points, L: dlib.points) -> None
        Extend the list by appending all the items in the given list

    extend(self: dlib.points, arg0: list) -> None
    insert(self: dlib.points, i: int, x: dlib.point) → None
    Insert an item at a given position.

    pop(*args, **kwargs)
        Overloaded function.

    pop(self: dlib.points) -> dlib.point
        Remove and return the last item

    pop(self: dlib.points, i: int) -> dlib.point
        Remove and return the item at index i

    remove(self: dlib.points, x: dlib.point) → None
        Remove the first item from the list whose value is x. It is an error if there is no such item.

    resize(self: dlib.points, arg0: int) → None
```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。
