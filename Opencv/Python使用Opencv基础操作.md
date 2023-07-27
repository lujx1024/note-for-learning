---
title: Python使用Opencv基础操作
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---

* [环境安装](#环境安装)
	* [安装依赖](#安装依赖)
	* [环境校验](#环境校验)
* [图像基础操作](#图像基础操作)
	* [读取图片](#读取图片)
	* [展示图片](#展示图片)
	* [保存图片](#保存图片)
	* [小结](#小结)
* [视频基础操作](#视频基础操作)
	* [读取摄像头视频流](#读取摄像头视频流)
	* [视频属性获取](#视频属性获取)
	* [读取视频文件](#读取视频文件)
* [opencv绘制图形](#opencv绘制图形)
	* [画线](#画线)
	* [画矩形](#画矩形)
	* [画圆形](#画圆形)
	* [写文本(中英文)](#写文本中英文)
		* [添加英文文本](#添加英文文本)
		* [添加中文文本](#添加中文文本)
	* [小结](#小结)

# 环境安装
## 安装依赖
`Windows`平台使用`pip`工具安装`opencv-python`即可，推荐使用`虚拟环境`，安装指令:`pip install opencv-python`

## 环境校验
键入指令进入`python`控制台环境(本实例是`虚拟环境` `quickstart`)，操作指令如下:

```
# 进入 虚拟环境
(quickstart)C:\Users\administrator  python -q

# 导入CV
>>> from cv2 import cv2

# 查看版本

>>> cv2.__version__
'4.5.3'
```
# 图像基础操作
## 读取图片
使用**cv.imread**()函数读取图像。函数原型是：
```
imread(filename, flags=None)
filename : 文件的相对或绝对路径
flags : 标识符，指定图片的读取方式
```
标志符分类：
- `IMREAD_COLOR` : 加载彩色图像。任何图像的透明度都会被忽视。它是默认标志
- `IMREAD_GRAYSCALE` : 以灰度模式加载图像
- `IMREAD_UNCHANGED` :  加载图像，包括alpha通道
> 除了这三个标志，也可以分别简单地传递整数1、0或-1

代码示例：
```
from cv2 import cv2 as cv

frame = cv.imread('ZA-wp6.jpg', cv.IMREAD_UNCHANGED)
```

## 展示图片
使用函数`cv.imshow(winname, mat)`在窗口中显示图像。窗口自动适合图像尺寸。
- 第一个参数是窗口名称，它是一个字符串。
- 第二个参数是我们的展示的图片帧对象。

可以根据需要创建任意多个窗口，但可以使用不同的窗口名称

示例代码：
```
frame = cv.imread('ZA-wp6.jpg', cv.IMREAD_UNCHANGED)

cv.imshow('frame', frame)
cv.waitKey(0)
cv.destroyAllWindows()
```
  `cv.waitKey()`是一个键盘绑定函数。其参数是以`毫秒`为单位的时间。该函数等待任何键盘事件指定
的毫秒。如果您在这段时间内按下任何键，程序将继续运行。如果`0`被传递，它将`无限期地等
待`一次敲击键。它也可以设置为检测特定的按键，例如，如果按下键 `a` 等，我们将在下面讨论。

> 注意 除了键盘绑定事件外，此功能还处理许多其他GUI事件，因此你必须使用它来实际显示图
像。

`cv.destroyAllWindows()`只会破坏我们创建的所有窗口。如果要销毁任何特定的窗口，请使用函
数`cv.destroyWindow()`在其中`传递确切的窗口名称`作为参数。

> 注意 在特殊情况下，你可以创建一个空窗口，然后再将图像加载到该窗口。在这种情况下，可以指定窗口是否可调整大小。这是通过功能**cv.namedWindow**()完成的。默认情况下，该标志为**cv.WINDOW_AUTOSIZE**。但是，如果将标志指定为**cv.WINDOW_NORMAL**，则可以调整窗口大小。当图像尺寸过大以及向窗口添加跟踪栏时，这将很有帮助。

## 保存图片

使用函数`imwrite(filename, img, params=None)`保存图像。
- 第一个参数是文件名
- 第二个参数是要保存的图像
 `cv.imwrite('messigray.png'，img)` 这会将图像以PNG格式保存在工作目录中.

 ## 小结
 在下面的程序中，以灰度加载图像，显示图像，按 `s` 保存图像并退出，或者按 `ESC`键直接退出而
不保存
 ```
 from cv2 import cv2 as cv
 
 img = cv.imread('ZA-wp6.jpg', cv.IMREAD_GRAYSCALE)

cv.imshow('image', img)
k = cv.waitKey(0) & 0xff
if k == 27:  # 等待ESC退出
    cv.destroyAllWindows()
elif k == ord('s'):  # 等待关键字，保存和退出
    cv.imwrite('test.png', img)
cv.destroyAllWindows()
 ```
# 视频基础操作

## 读取摄像头视频流
要捕获视频，需要创建一个 `VideoCapture `对象。它的参数可以是`设备索引`或`视频文件的名
称`。设备索引就是指定哪个摄像头的数字。正常情况下，一个摄像头会被连接(就像我的情况一
样)。所以我简单地传0(或-1)。你可以通过传递1来选择第二个相机，以此类推。在此之后，你可以
逐帧捕获。但是在最后，不要忘记释放内存。

示例代码：

```
from cv2 import cv2 as cv

cap = cv.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    # 如果正确读取帧，ret为True
    if ret:
    	cv.imshow('frame', frame)
    if cv.waitKey(5) & 0xff == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
```

## 视频属性获取
你还可以使用`cap.get(propId)` 方法访问该视频的某些功能，其中`propId`是`0`到`18`之间的一个数字。每个数字表示视频的属性（如果适用于该视频），并且可以显示完整的详细信息在这里看到：`cv::VideoCapture::get()`。其中一些值可以使用 `cap.set(propId，value)` 进行修改。 value是你想要的新值。
例如，我可以通过 `cap.get(cv.CAP_PROP_FRAME_WIDTH)`和 `cap.get(cv.CAP_PROP_FRAME_HEIGHT)`检查框架的`宽度`和`高度`。
默认情况下，它的分辨率为`640x480`。但我想将其修改为`320x240`。只需如下设置即可。 
```
ret = cap.set(cv.CAP_PROP_FRAME_WIDTH,320) 
ret = cap.set(cv.CAP_PROP_FRAME_HEIGHT,240)
```

## 读取视频文件
与捕获摄像头视频流基本相同，只需将摄像头设备索引更换为视频文件路径即可。
```
from cv2 import cv2 as cv

cap = cv.VideoCapture('MrBean.mp4')
while cap.isOpened():
    ret, frame = cap.read()
    # 如果正确读取帧，ret为True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv.imshow('frame', frame)

    if cv.waitKey(5) & 0xff == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
```

> 在显示图像窗口时，请使用适当的时间 `cv.waitKey()` 。如果太小，则视频将非常快，而如果太大，则视频将变得很慢（嗯，这就是显示慢动作的方式）。正常情况下`25`毫秒就可以了.

保存视频
我们捕捉一个视频，一帧一帧地处理，我们想要保存这个视频。对于图像，它非常简单，只需使用`cv.imwrite()`。创建一个 `VideoWriter `对象。指定输出文件名(例如: output.avi)。然后指定 `FourCC `代码,传递帧率的数量和帧大小。最后一个是`颜色标志`。如果为`True `，编码器将处理为`颜色帧`，否则为`灰度帧`。

```
from cv2 import cv2 as cv

cap = cv.VideoCapture('MrBean.mp4')
fourcc = cv.VideoWriter_fourcc(*'mp4v')
out = cv.VideoWriter("out.mp4", fourcc, 20.0, (640, 480))
while cap.isOpened():
    ret, frame = cap.read()
    # 如果正确读取帧，ret为True
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    # gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
	
	# 将图像上下翻转
    frame = cv.flip(frame, 0)

    cv.imshow('frame', frame)
    out.write(frame)
    if cv.waitKey(5) & 0xff == ord('q'):
        break
cap.release()
cv.destroyAllWindows()
```
- 在`Fedora`中：`DIVX`，`XVID`，`MJPG`，`X264`，`WMV1`，`WMV2`。（最好使用`XVID`。`MJPG`会生成大尺寸的视频。`X264`会生成非常小的尺寸的视频）
- 在`Windows`中：`DIVX`（尚待测试和添加）
- 在`OSX`中：`MJPG`（`.mp4`），`DIVX`（`.avi`），`X264`（`.mkv`）。
`FourCC`代码作为`MJPG`的 `cv.VideoWriter_fourcc('M'，'J'，'P'，'G')` or `cv.VideoWriter_fourcc(*'MJPG')` 传递。

# opencv绘制图形

学习使用OpenCV绘制不同的几何形状
主要功能：`cv.line()`，`cv.circle()`，`cv.rectangle()`，`cv.ellipse()`，`cv.putText()`等。
常见的参数，如下所示：
- img：您要绘制形状的图像
- color：形状的颜色。对于BGR，将其作为元组传递，例如：(255,0,0)对于蓝色。对于灰度，只需传递标量值即可。
- thickness(厚度)：线或圆等的粗细。如果对闭合图形（如圆）传递 -1 ，它将填充形状。默认厚度= 1
- lineType：线的类型，是否为8连接线，抗锯齿线等。默认情况下，为8连接线。**cv.LINE_AA**给出了抗锯齿的线条，看起来非常适合曲线。


## 画线

绘制一条线，使用`cv2.line()` 。
参数解析：
- img : 图像，数据类型 numpy.ndarray
- pt1 : 起始点坐标，数据类型 元组,成员为点的横纵坐标,如(0,0)
- pt2 : 结束点坐标，数据类型 元组,成员为点的横纵坐标,如(100,100)
- color ：线条颜色，数据类型 元组 按照BGR排列 例如(255,0,0)
- thickness : 线或圆等的粗细
- lineType ： 线的类型

方法您需要传递线的开始和结束坐标。我们将创建一个黑色图像，并从左上角到右下在其上绘制一条蓝线。
```
import numpy as np
from cv2 import cv2

img = np.zeros((512, 512, 3), np.uint8)
cv2.line(img, (0, 0), (150, 150), (255, 0, 0), 2)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

## 画矩形

方法：
`cv2.rectangle()`

参数解析：
- img : 图像，数据类型 numpy.ndarray
- pt1 : 矩形点坐标，数据类型 元组,成员为点的横纵坐标,如(0,0)
- pt2 : 矩形点坐标，数据类型 元组,成员为点的横纵坐标,如(100,100)
- color ：线条颜色，数据类型 元组 按照BGR排列 例如(255,0,0)
- thickness : 线或圆等的粗细
- lineType ： 线的类型


代码示例：

`cv2.rectangle(img,(384,0),(510,128),(0,255,0),3)`

## 画圆形
方法 :
`cv2.circle()`

参数解析 :
- img : 图像，数据类型 numpy.ndarray
- center: 圆心点坐标，数据类型 元组,成员为点的横纵坐标,如(50,50)
- radius: 半径
- color ：线条颜色，数据类型 元组 按照BGR排列 例如(255,0,0)
- thickness : 线或圆等的粗细
- lineType ： 线的类型

代码示例：

`cv2.circle(img, (447, 63), 63, (0, 0, 255), -1)`

## 写文本(中英文)

### 添加英文文本
opencv-python支持在图像中直接写入英文，

方法：
`cv2.putText(img, text, org, fontFace, fontScale, colore)`

参数解析：
- img : 图像，数据类型 numpy.ndarray
- text : 写入的文本，数据类型 string
- org : 文字的左下角的点坐标，数据类型 元组,成员为点的横纵坐标,如(50,50)
- fontFace ：字体类型，数据类型 元组 按照BGR排列 例如(255,0,0)
- fontScale ：字体比例或字体大小
- color ：线条颜色，数据类型 元组 按照BGR排列 例如(255,0,0)
- thickness : 线或圆等的粗细
- lineType ： 线的类型

代码示例：

```
font = cv.FONT_HERSHEY_SIMPLEX
cv.putText(img,'OpenCV',(10,500), font, 4,(255,255,255),2,cv.LINE_AA)
```

### 添加中文文本

opencv-python不支持直接写入中文字符，强行写入会导致乱码，以下记录写入中文字符的方法：

1. 安装pillow依赖库 ：`pip install pillow`
2. 使用pillow依赖库，转化图片数据，并写入文本
3. 将数据格式转为cv2格式返回已写入文本的图像数据

示例代码如下：

```
from PIL import Image, ImageDraw, ImageFont


def putTextOnImg(img, text, org, color, fontsize):
    """
    putTextOnImg(img, text, org, color [, fontsize]) -> img
    .   @brief Draws a non-alphabet text string.
    .
    .   This function read the image data from cv2 using pillow::Image::fromarray and put a non-alphabet text like
    .   Chinese on the Image ,and then return the image as numpy::ndarray,just like the original parameter.
    .
    .   @param img Image.
    .   @param text Text string to be drawn.
    .   @param org Bottom-left corner of the text string in the image.
    .   @param color Text color.
    .   @param fontsize Font scale factor that is multiplied by the font-specific base size.
    """

    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    font_style = ImageFont.truetype("font/simsun.ttc", fontsize, encoding='utf-8')
    draw.text(org, text, font=font_style, fill=color)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)
```
使用示例：
`img = putTextOnImg(img, "你好", (50, 150), (255, 0, 0), 30)`

## 小结

一下是opencv-python画直线、矩形、圆形以及写入文本的代码小结.
```
import numpy as np
from cv2 import cv2
from PIL import Image, ImageDraw, ImageFont


def putTextOnImg(img, text, org, color, fontsize):
    """
    putTextOnImg(img, text, org, color [, fontsize]) -> img
    .   @brief Draws a non-alphabet text string.
    .
    .   This function read the image data from cv2 using pillow::Image::fromarray and put a non-alphabet text like
    .   Chinese on the Image ,and then return the image as numpy::ndarray,just like the original parameter.
    .
    .   @param img Image.
    .   @param text Text string to be drawn.
    .   @param org Bottom-left corner of the text string in the image.
    .   @param color Text color.
    .   @param fontsize Font scale factor that is multiplied by the font-specific base size.
    """

    img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img)
    font_style = ImageFont.truetype("font/simsun.ttc", fontsize, encoding='utf-8')
    draw.text(org, text, font=font_style, fill=color)
    return cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

# 创建图像
img = np.ones((512, 512, 3), np.uint8)
# 画直线
cv2.line(img, (0, 0), (150, 150), (255, 0, 0), 2)
# 画矩形
cv2.rectangle(img, (384, 0), (510, 128), (0, 255, 0), 3)
# 画圆
cv2.circle(img, (447, 63), 63, (0, 0, 255), -1)
# 写入英文文本
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(img, 'OpenCV', (10, 500), font, 4, (255, 255, 255), 2, cv2.LINE_AA)
# 写入中文文本，返回图像数据
img = putTextOnImg(img, "你好", (50, 150), (255, 0, 0), 30)
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。