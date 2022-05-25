---
title: dlib实现人脸检测方法 
tags: dlib,人脸检测,Python
renderNumberedHeading: true
grammar_cjkRuby: true
---
[toc]
# `dlib`概述
`Dlib`是一个包含机器学习算法的`C++`开源工具包。`Dlib`可以帮助您创建很多复杂的机器学习方面的软件来帮助解决实际问题。目前`Dlib`已经被广泛的用在行业和学术领域，包括机器人，嵌入式设备，移动电话和大型高性能计算环境.

# 人脸检测

## CPU版本人脸检测算法

### 检测步骤

1. 获取hog detector
2. 传入image,数据格式为numpy.ndarray
3. (可选项) 获取分数值和检测列表
4. 获取人脸坐标

### 示例代码：

```
import dlib

from cv2 import cv2

# step 1. create an object detector based on hog
detector = dlib.get_frontal_face_detector()  # _dlib_pybind11.fhog_object_detector

# step 2. read an image using dlib or cv2
# note that the difference between the image data formated as numpy.ndarray read by dlib and cv2 is that dlib read it channels as *R G B* order while cv2 read as *B G R*,so you should do one more step to convert the image if using cv2
image_path = "sample.jpg"
img = dlib.load_rgb_image(image_path)
# img = cv2.imread(image_path)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# step 3. using the numpy.ndarray image data as input to detect the front face on the image
# The 1 in the second argument indicates that we should upsample the image 1 time.  
# This will make everything bigger and allow us to detect more faces.
detections = detector(img, 1) # List[_dlib_pybind11.rectangle]

# step 3.1 (Optional) if you want to get more detail information,using function run() instead
# detections, scores, idx = detector.run(img, 1, 0.5) # List[_dlib_pybind11.rectangle] List[int] List[int]

# step 4. get point coordinates from the detection results
# let's just fetch one instead all of the in a loop
detection = detections[0]
left,top,right,bottom = detection .left(),detection .top(),detection .right(),detection .bottom()

# step x : now you can do whatever you want since you've already got what you want.
```

## CUDA版本人脸检测算法

### 检测步骤
1. 下载模型文件
2. 加载模型文件，生成卷积神经网络人脸检测对象
3. 传入image,数据格式为numpy.ndarray
4. (可选项) 获取分数值和检测列表
5.  获取人脸坐标

### 示例代码

```
import dlib
# step 1. make sure you have downloaded the correct model file
face_detector_model_path = '../models/mmod_human_face_detector.dat'

# step 2. load this model and create a cnn face detector
face_detector = dlib.cnn_face_detection_model_v1(face_detector_model_path)  # dlib.cnn_face_detection_model_v1

# step 3. read an image using dlib or cv2
# note that the difference between the image data formated as numpy.ndarray read by dlib and cv2 is that dlib read it channels as *R G B* order while cv2 read as *B G R*,so you should do one more step to convert the image if using cv2
image_path = "sample.jpg"
img = dlib.load_rgb_image(image_path)
# img = cv2.imread(image_path)
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

# step 4. predict and detect
detections = face_detector(img, 1)  # dlib.mmod_rectangles

# step 5. get just one of the rectangle instead all of them ,the type is mmod_rectangle
detection = detections[0]  # dlib.mmod_rectangle
# the mmod_rectangle contains two parts : confidence and rect
print(detection.confidence, detection.rect)

# step 6.get face coordinates for just one as sample
left,top,right,bottom = detection.rect.left(),detection.rect.top(),detection.rect.right(),detection.rect.bottom()

# step x. do anything you would like to
```



## 类定义与接口源码
### 人脸检测中用到的重要的类(概述)
 1.  `dlib.fhog_object_detector` : hog模型的人脸检测对象,常用方法: `__call()__`和`run()`
 2.  `dlib.rectangle`:人脸检测结果，用于表示人脸的矩形区域,常用方法：`left()` `right()``top()``bottom()`
 3.  `dlib.cnn_face_detection_model_v1`:卷积神经网络模型的人脸检测对象,常用方法: `__call()__`
 4.  `dlib.mmod_rectangle`:人脸检测结果，包含了表示人脸的巨型区域以及检测置信度,成员包含: `rect`和`confidence`,其中,`rect`为  `dlib.rectangle`类型,`confidence`为`float`类型
 5.  `dlib.mmod_rectangles`:包含多个 `dlib.mmod_rectangle`对象

类定义参考链接：[Python API 链接](http://dlib.net/python/index.html)

### `fhog_object_detector`类接口定义

`fhog_object_detector`类在源码中为C++类，这里使用伪代码编译观察其接口与调用方法

```
class dlib.fhog_object_detector():
    """
    This object represents a sliding window histogram-of-oriented-gradients based object detector.
    """

    def __call__(self: dlib.fhog_object_detector, image: array, upsample_num_times: int = 0L) -> dlib.rectangles:
        """
        requires
        image is a numpy ndarray containing either an 8bit grayscale or RGB image.
        upsample_num_times >= 0
        ensures
        This function runs the object detector on the input image and returns a list of detections.
        Upsamples the image upsample_num_times before running the basic detector.
        """
    def __init__(self: dlib.fhog_object_detector, arg0: unicode) -> None:
        '''
        Loads an object detector from a file that contains the output of the train_simple_object_detector() routine or a serialized C++ object of type object_detector<scan_fhog_pyramid<pyramid_down<6>>>.
        detection_window_height
        detection_window_width
        num_detectors
        '''
        pass

    def run(self: dlib.fhog_object_detector, image: array, upsample_num_times: int = 0L,
            adjust_threshold: float = 0.0) -> tuple:
        """
        requires
        image is a numpy ndarray containing either an 8bit grayscale or RGB image.
        upsample_num_times >= 0
        ensures
        This function runs the object detector on the input image and returns a tuple of (list of detections, list of scores, list of weight_indices).
        Upsamples the image upsample_num_times before running the basic detector.
        """
        pass

    def run_multiple(detectors: list, image: array, upsample_num_times: int = 0L, adjust_threshold: float = 0.0)->tuple:
        """
        requires
        detectors is a list of detectors.
        image is a numpy ndarray containing either an 8bit grayscale or RGB image.
        upsample_num_times >= 0
        ensures
        This function runs the list of object detectors at once on the input image and returns a tuple of (list of detections, list of scores, list of weight_indices).
        Upsamples the image upsample_num_times before running the basic detector.
        """
        pass

    def save(self: dlib.fhog_object_detector, detector_output_filename: unicode)->None:
        '''
        Save a simple_object_detector to the provided path.
        '''
        pass
```

### `rectangle`类接口定义
```
class dlib.rectangle
    This object represents a rectangular area of an image.

    __init__(*args, **kwargs)
        Overloaded function.

        __init__(self: dlib.rectangle, left: int, top: int, right: int, bottom: int) -> None
        __init__(self: dlib.rectangle, rect: dlib::drectangle) -> None
        __init__(self: dlib.rectangle, rect: dlib.rectangle) -> None
        __init__(self: dlib.rectangle) -> None
    area(self: dlib.rectangle) → int
    bl_corner(self: dlib.rectangle) → dlib.point
        Returns the bottom left corner of the rectangle.

    bottom(self: dlib.rectangle) → int
    br_corner(self: dlib.rectangle) → dlib.point
        Returns the bottom right corner of the rectangle.

    center(self: dlib.rectangle) → dlib.point
    contains(*args, **kwargs)
        Overloaded function.

        contains(self: dlib.rectangle, point: dlib.point) -> bool
        contains(self: dlib.rectangle, point: dlib.dpoint) -> bool
        contains(self: dlib.rectangle, x: int, y: int) -> bool
        contains(self: dlib.rectangle, rectangle: dlib.rectangle) -> bool
        dcenter(self: dlib.rectangle) → dlib.point
    height(self: dlib.rectangle) → int
    intersect(self: dlib.rectangle, rectangle: dlib.rectangle) → dlib.rectangle
    is_empty(self: dlib.rectangle) → bool
    left(self: dlib.rectangle) → int
    right(self: dlib.rectangle) → int
    tl_corner(self: dlib.rectangle) → dlib.point
        Returns the top left corner of the rectangle.

    top(self: dlib.rectangle) → int
    tr_corner(self: dlib.rectangle) → dlib.point
        Returns the top right corner of the rectangle.

    width(self: dlib.rectangle) → int
```
### `cnn_face_detection_model_v1`类定义

```
class dlib.cnn_face_detection_model_v1
    This object detects human faces in an image. The constructor loads the face detection model from a file. You can download a pre-trained model from http://dlib.net/files/mmod_human_face_detector.dat.bz2.

    __call__(*args, **kwargs)
    Overloaded function.
    
    __call__(self: dlib.cnn_face_detection_model_v1, imgs: list, upsample_num_times: int=0L, batch_size: int=128L) -> std::vector<std::vector<dlib::mmod_rect, std::allocator<dlib::mmod_rect> >, std::allocator<std::vector<dlib::mmod_rect, std::allocator<dlib::mmod_rect> > > >
    takes a list of images as input returning a 2d list of mmod rectangles
    
    __call__(self: dlib.cnn_face_detection_model_v1, img: array, upsample_num_times: int=0L) -> std::vector<dlib::mmod_rect, std::allocator<dlib::mmod_rect> >
    Find faces in an image using a deep learning model.
    Upsamples the image upsample_num_times before running the face detector.
    
    __init__(self: dlib.cnn_face_detection_model_v1, filename: unicode) → Non
```



### `mmod_rectangle` `mmod_rectangles` `mmod_rectangless`
```
class dlib.mmod_rectangle
    Wrapper around a rectangle object and a detection confidence score.
    
    __init__
    x.__init__(...) initializes x; see help(type(x)) for signature
    
    confidence
    rect
```

```
class dlib.mmod_rectangles
    An array of mmod rectangle objects.
    
    __init__(*args, **kwargs)
    Overloaded function.
    
    __init__(self: dlib.mmod_rectangles) -> None
    __init__(self: dlib.mmod_rectangles, arg0: dlib.mmod_rectangles) -> None
    Copy constructor
    
    __init__(self: dlib.mmod_rectangles, arg0: iterable) -> None
    append(self: dlib.mmod_rectangles, x: dlib.mmod_rectangle) → None
    Add an item to the end of the list
    
    count(self: dlib.mmod_rectangles, x: dlib.mmod_rectangle) → int
    Return the number of times x appears in the list
    
    extend(*args, **kwargs)
    Overloaded function.
    
    extend(self: dlib.mmod_rectangles, L: dlib.mmod_rectangles) -> None
    Extend the list by appending all the items in the given list
    
    extend(self: dlib.mmod_rectangles, arg0: list) -> None
    insert(self: dlib.mmod_rectangles, i: int, x: dlib.mmod_rectangle) → None
    Insert an item at a given position.
    
    pop(*args, **kwargs)
    Overloaded function.
    
    pop(self: dlib.mmod_rectangles) -> dlib.mmod_rectangle
    Remove and return the last item
    
    pop(self: dlib.mmod_rectangles, i: int) -> dlib.mmod_rectangle
    Remove and return the item at index i
    
    remove(self: dlib.mmod_rectangles, x: dlib.mmod_rectangle) → None
    Remove the first item from the list whose value is x. It is an error if there is no such item.
```
```
class dlib.mmod_rectangless
    A 2D array of mmod rectangle objects.
    
    __init__(*args, **kwargs)
    Overloaded function.
    
    __init__(self: dlib.mmod_rectangless) -> None
    __init__(self: dlib.mmod_rectangless, arg0: dlib.mmod_rectangless) -> None
    Copy constructor
    
    __init__(self: dlib.mmod_rectangless, arg0: iterable) -> None
    append(self: dlib.mmod_rectangless, x: dlib.mmod_rectangles) → None
    Add an item to the end of the list
    
    count(self: dlib.mmod_rectangless, x: dlib.mmod_rectangles) → int
    Return the number of times x appears in the list
    
    extend(*args, **kwargs)
    Overloaded function.
    
    extend(self: dlib.mmod_rectangless, L: dlib.mmod_rectangless) -> None
    Extend the list by appending all the items in the given list
    
    extend(self: dlib.mmod_rectangless, arg0: list) -> None
    insert(self: dlib.mmod_rectangless, i: int, x: dlib.mmod_rectangles) → None
    Insert an item at a given position.
    
    pop(*args, **kwargs)
    Overloaded function.
    
    pop(self: dlib.mmod_rectangless) -> dlib.mmod_rectangles
    Remove and return the last item
    
    pop(self: dlib.mmod_rectangless, i: int) -> dlib.mmod_rectangles
    Remove and return the item at index i
    
    remove(self: dlib.mmod_rectangless, x: dlib.mmod_rectangles) → None
    Remove the first item from the list whose value is x. It is an error if there is no such item.
```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。
