---
title: dlib实现人脸对齐方法 
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---
# 操作步骤
1. 人脸检测
2. 人脸关键点检测
3. 人脸对齐

# 关键类与接口方法定义

## 类

1. 人脸检测类 :  `dlib.fhog_object_detector`和 `dlib.cnn_face_detection_model_v1`,前者基于HOG模型，后者基于CNN模型，前者检测方法调用为`__call(img)__ ->dlib.rectangles`和`run(img,upsample_num,threshold)->(dlib.rectangles,List[scores:int],List[int])`,后者检测方法调用为`__call(img)__->dlib.mmod_rectangles`
2. 关键点检测类: `dlib.shape_predictor`,预测调用方法`__call__(self,image, box: dlib.rectangle)->dlib.full_object_detection`
3. 检测结果类 : `dlib.full_object_detection`， 常用方法 `part(self, idx: int)->dlib.point` 单个关键点信息 、`parts(self)->dlib.points` 所有的关键点信息
4. 关键点类：`dlib.point`关键点，成员包含x，y，`dlib.points`关键点列表

## 方法
1. 获取单个人脸对齐结果 
	>  padding参数可调整图像返回值的尺寸大小
```
get_face_chip(img: numpy.ndarray[(rows,cols,3),uint8], face: _dlib_pybind11.full_object_detection, size: int=150, padding: float=0.25) -> numpy.ndarray[(rows,cols,3),uint8]

Takes an image and a full_object_detection that references a face in that image and returns the face as a Numpy array representing the image.  The face will be rotated upright and scaled to 150x150 pixels or with the optional specified size and padding.
```
2. 获取多个人脸对齐结果
  ```
  get_face_chips(img: numpy.ndarray[(rows,cols,3),uint8], faces: _dlib_pybind11.full_object_detections, size: int=150, padding: float=0.25)->list
    
    Takes an image and a full_object_detections object that reference faces in that image and returns the faces as a list of Numpy arrays representing the image.  The faces will be rotated upright and scaled to 150x150 pixels or with the optional specified size and padding.
    
  ```

# 示例代码

```
import dlib
import numpy as np

from cv2 import cv2

# step 1. create face detect and shape predict model
face_detector_model_path = '../models/mmod_human_face_detector.dat'
face_detector = dlib.cnn_face_detection_model_v1(face_detector_model_path)  # dlib.cnn_face_detection_model_v1
shape_model_path = r'../models/shape_predictor_68_face_landmarks.dat'
face_shape_predictor = dlib.shape_predictor(shape_model_path)  # dlib.shape_predictor

# step 2. get all face detections
image_path = "sample.jpg"
img = dlib.load_rgb_image(image_path)
detections = face_detector(img, 1)  # dlib.mmod_rectangles

# step 3. fetch one of all face detections, and if it's mmod_rectangle , convert to rectabgle
detection = detections[0]  # dlib.mmod_rectangle
# the mmod_rectangle contains two parts : confidence and rect

# step 4. get one face shape and return a single object name full_object_detection
shape = face_shape_predictor(img, detection.rect)  # dlib.full_object_detection

# step 5. get one aligned face 
image = dlib.get_face_chip(img, shape, size=150, padding=0.45) # numpy.ndarray

# Optionally: get all the aligned faces that was detected in the first place
faces = [face.rect for face in detections]
# Get the aligned face images
# faces = dlib.full_object_detections()
# faces.append(shape)
# Optionally:
images = dlib.get_face_chips(img, faces, size=160, padding=0.25)
```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。