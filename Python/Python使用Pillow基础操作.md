---
title: Python使用Pillow基础操作
tags: Python,Pillow,使用手册
renderNumberedHeading: true
grammar_cjkRuby: true
---
# 环境安装

> 请注意 : `Pillow`和`PIL`在同一个环境中不兼容，所以在安装`Pillow`之前需确认是否已安装,如已安装`PIL`，在安装`Pillow`之前卸载`PIL`

使用`pip`工具安装`Pillow`:
`python3 -m pip install --upgrade Pillow` 或者 `pip install pillow`

# 基础功能

## `Image `类的使用

### 图像读取

 `Image `类是Pillow(PIL)库中最为重要的类,模块名称为`PIL.Image`.`Image`可通过多种方式实例化;可通过加载文件实例化, 处理其他图片的过程中实例化, 或者干脆直接创建一个`Image`对象。.

`Image`模块使用 `open()` 方法加载图片生成对象:

```
from PIL import Image

img = Image.open("magic.jpg")
print(img.format, img.size, img.mode)

# 输出：图片的编码格式、像素大小、颜色格式
# JPEG (1920, 1080) RGB
```
## 图像显示

`Image`类定义了`show()`方法用于图片展示：

`img.show()`

> 标准版 show() 方法的效率并不高, 因为它首先保存了一个临时文件在本地，然后调用了图像显示工具来实现显示功能，所以，如果本地并没有正确安装此类工具，图像将无法显示.但是如果可以正常展示图片的话，会给调试和测试带来很多便利。

## 图像读写

### 图像格式转化

```
from PIL import Image

origin_file = 'magic.jpg'
target_file = "magic.png"

try:
	with Image.open(origin_file) as img:
		# 图片保存
		img.save(target_file)
except OSError:
	print("cannot convert", origin_file)
```
### 创建缩略图

```
from PIL import Image

# 定义缩略图大小
size = (128, 128)
origin_file = "magic.jpg"
thumbnail_file = "magic_thumbnail.jpg"
try:
    with Image.open(origin_file) as img:
        # 创建缩略图
        img.thumbnail(size)
        # 保存缩略图
        img.save(thumbnail_file, "JPEG")
except OSError:
    print("cannot create thumbnail for", origin_file)
```
### 图片的裁剪、粘贴与合并

`Image`类包含一些可以操作图像内区域的方法，使用`crop()`方法可从图像中剪切出一块矩形区域。

**图像裁剪**
区域坐标由一个4个成员的元组定义，分别代表左上角和右下角的坐标点，`PIL `库默认图像的左上角为原点，即(0,0)点 .
```
from PIL import Image

origin_file = "magic.jpg"
try:
    with Image.open(origin_file) as img:
        # 定义裁剪区域坐标点(左上角和右下角)
        box = (100, 100, 400, 400)
        region = img.crop(box)
except OSError:
    print("cannot read from ", origin_file)
```

**图像的旋转与粘贴**

`Image`类提供了图像翻转的方法`Image.transpose()`,预定义参数有：

- `PIL.Image.FLIP_LEFT_RIGHT` ： 左右翻转
- `PIL.Image.FLIP_TOP_BOTTOM` ： 上下翻转
- `PIL.Image.ROTATE_90` ： 旋转90°
- `PIL.Image.ROTATE_180` ： 旋转180°
- `PIL.Image.ROTATE_270` ： 旋转270°

> 使用`Image.paste()`方法须确保裁剪的区域与粘贴的区域与大小坐标完全一致，否则会报错
```
from PIL import Image
from PIL.JpegImagePlugin import JpegImageFile
origin_file = "magic.jpg"
try:
    with Image.open(origin_file) as img:
        # 定义裁剪区域坐标点(左上角和右下角)
        box = (100, 100, 400, 400)
        region = img.crop(box)

        region = region.transpose(Image.ROTATE_180)
        img.paste(region, box)

        img.show()
except OSError:
    print("cannot read from ", origin_file)
```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。