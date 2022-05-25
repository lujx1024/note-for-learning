---
title: dlib实现人脸识别方法
tags: dlib,face recognition,Python
renderNumberedHeading: true
grammar_cjkRuby: true
---

# 概述

此示例演示如何使用dlib作为人脸识别工具，dlib提供一个方法可将人脸图片数据映射到128维度的空间向量，如果两张图片来源于同一个人，那么两个图片所映射的空间向量距离就很近，否则就会很远。因此，可以通过提取图片并映射到128维空间向量再度量它们的欧氏距离(Euclidean distance)是否足够小来判定是否为同一个人。

当设置向量距离阈值为0.6时，2007年，在与其他先进的人脸识别方法的比赛中，dlib模型在LFW人脸数据集基线测试准确率为99.38%。这个准确率意味着,在判断一对照片是否为同一个人时，dlib工具将具有99.38%的准确率。

# 方法实现

## 实现步骤
1. 实例化人脸检测模型、人脸关键点检测模型、人脸识别模型
2. 加载一对图片
3. 分别获取图片中的人脸图片所映射的空间向量，即人脸特征值
4. 计算特征向量欧氏距离，根据阈值判断是否为同一个人

## 示例代码
```
import sys
import os
import dlib
import glob
import numpy as np

def find_euclidean_distance(source_representation, test_representation):
    """
    计算向量的欧氏距离
    """
    euclidean_distance = source_representation - test_representation
    euclidean_distance = np.sum(np.multiply(euclidean_distance, euclidean_distance))
    euclidean_distance = np.sqrt(euclidean_distance)
    return euclidean_distance

# 加载模型
face_detect_model_path = '../models/mmod_human_face_detector.dat'
face_shape_predictor_path = '../models/shape_predictor_5_face_landmarks.dat'
face_rec_model_path = '../models/dlib_face_recognition_resnet_model_v1.dat'
face_detector = dlib.cnn_face_detection_model_v1(face_detect_model_path)
face_shape_predictor = dlib.shape_predictor(face_shape_predictor_path)
face_recognition_model = dlib.face_recognition_model_v1(face_rec_model_path)

image_path = r'sample1.jpg'
image_cmp_path = r'sample12.jpg'
image=dlib.load_rgb_image(image_path)
image_cmp = dlib.load_rgb_image(image_cmp_path)

face_detections = face_detector(image, 1)
# 假定每张对比图片只有一张人脸
face_shape=face_shape_predictor(image, face_detections[0].rect)
# 获取人脸图片128维向量
face_descriptor = face_recognition_model.compute_face_descriptor(image,face_shape,10,0.35)
face_feature = np.array(face_descriptor)

# 获取对比人脸图片的128维向量
face_cmp_detections = face_detector(image_cmp, 1)
face_cmp_shape = face_shape_predictor(image_cmp, face_cmp_detections[0].rect)
face_cmp_descriptor = face_recognition_model.compute_face_descriptor(image_cmp, face_cmp_shape,10,0.35)
face_cmp_feature = np.array(face_cmp_descriptor)

# 获取向量欧式距离
distance = find_euclidean_distance(face_feature, face_cmp_feature)
print(distance)
```

获取人脸向量方法,可继续添加参数如下 :
`face_descriptor = face_recognition_model.compute_face_descriptor(img, shape, 100, 0.25)`
- 在LFW数据集测试中，不传入100这个参数，得到的正确率是99.13%，传入参数100，正确率为99.38%.然而，传入100这个参数,使得这个方法的执行速度慢了100倍，所以按需选择即可。进一步解释一下第三个参数，第三个参数用来告诉函数执行多少次人脸提取(jitter/resample),当设置为100时，会提取100次稍作修改的人脸图片并取平均值，再去映射为空间向量，这个数值可以设置小一点，例如 10，那么执行速度将会慢10倍而不是100倍，正确率却依然有99.3%.

- 第四个参数值padding(0.25)是人脸图形的内边距.设置padding为0将会沿着人脸区域剪切，padding值越大，剪切的图片将会向外延伸，padding设置为0.5时，图像宽度变为原来的2倍，padding设置为1时为三倍，以此类推.

## 重载方法
另外一种获取人脸特征向量的方法(直接传入已对齐的人脸图片)：
```
# 获取人脸对齐图片，必须是默认的尺寸(150*150)
face_chip = dlib.get_face_chip(img, shape)

# 获取特征向量
face_feature_from_prealigned_image = face_recognition_model.compute_face_descriptor(face_chip)
```

重载方法汇总：
```
1. compute_face_descriptor(self, img: numpy.ndarray[(rows,cols,3),uint8], face: dlib.full_object_detection, num_jitters: int=0, padding: float=0.25) -> dlib.vector

    Takes an image and a full_object_detection that references a face in that image and converts it into a 128D face descriptor. 
    If num_jitters>1 then each face will be randomly jittered slightly num_jitters times, each run through the 128D projection, and the average used as the face descriptor.
    Optionally allows to override default padding of 0.25 around the face.

2. compute_face_descriptor(self, img: numpy.ndarray[(rows,cols,3),uint8], num_jitters: int=0) -> dlib.vector

    Takes an aligned face image of size 150x150 and converts it into a 128D face descriptor.
    Note that the alignment should be done in the same way dlib.get_face_chip does it.
    If num_jitters>1 then image will be randomly jittered slightly num_jitters times, each run through the 128D projection, 
    and the average used as the face descriptor. 

3. compute_face_descriptor(self, img: numpy.ndarray[(rows,cols,3),uint8], faces: dlib.full_object_detections, num_jitters: int=0, padding: float=0.25) -> dlib.vectors

    Takes an image and an array of full_object_detections that reference faces in that image and converts them into 128D face descriptors.  
    If num_jitters>1 then each face will be randomly jittered slightly num_jitters times, each run through the 128D projection, 
    and the average used as the face descriptor. Optionally allows to override default padding of 0.25 around the face.

4. compute_face_descriptor(self, batch_img: List[numpy.ndarray[(rows,cols,3),uint8]], batch_faces: List[dlib.full_object_detections], num_jitters: int=0, padding: float=0.25) -> dlib.vectorss

    Takes an array of images and an array of arrays of full_object_detections. `batch_faces[i]` must be an array of full_object_detections corresponding to the image `batch_img[i]`, referencing faces in that image. 
    Every face will be converted into 128D face descriptors.  
	If num_jitters>1 then each face will be randomly jittered slightly num_jitters times, each run through the 128D projection, and the average used as the face descriptor. 
    Optionally allows to override default padding of 0.25 around the face.

5. compute_face_descriptor(self, batch_img: List[numpy.ndarray[(rows,cols,3),uint8]], num_jitters: int=0) -> dlib.vectors

    Takes an array of aligned images of faces of size 150_x_150.Note that the alignment should be done in the same way dlib.get_face_chip does it.Every face will be converted into 128D face descriptors.  
    If num_jitters>1 then each face will be randomly jittered slightly num_jitters times, each run through the 128D projection, and the average used as the face descriptor.
```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。

