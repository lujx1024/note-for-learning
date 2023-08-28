[TOC]

# 概述

本文档主要描述`python`平台，使用`TensorRT`推理`YOLOv5`模型的方法。

文档主要包含以下内容：

- `tensorrt`库`Python API`的安装
- engine模型文件的导出说明
- tensorrt的基础API接口，包括`模型反序列化`，`模型参数获取`，`模型推理上下文构建`等
- 图片数据的预处理
- 推理结果后处理，包括`NMS`,`cxcywh`坐标转换为`xyxy`坐标等
- 关键方法的调用与参数说明
- 完整的示例代码

# 1.环境部署

## 预安装环境
1. `(Windows) Visual Studio 2019`
2. `CUDA 11.0` `CUDNN  8.2.x`
3. `Anaconda3` 或 `MiniConda3`
4. `Pytorch 1.7.1`
5. `onnx 1.11.0` 和 `onnxruntime-gpu 1.11.0 `

## 安装TensorRT

windows平台，安装`TensorRT`，需要先下载`TensorRT`的安装包，下载完成后，解压到指定目录，然后配置环境变量`TensorRT-8.x.x/lib`到环境变量`Path`即可。 

> TensorRT在Windows上的部署安装不在赘述，有专门的文档进行详细描述，这里安装的版本是 TensorRT 8.4.x

## 安装TensorRT的Python API

1. 创建虚拟环境

   ```shell
    conda create -n trt python=3.8 -y

    conda activate trt
    ```
2. 安装`TensorRT`的`Python API`，这里安装的版本是`TensorRT 8.4.x`

   ```shell
    cd TensorRT-8.x.x.x\python
    pip install tensorrt-8.4.3.1-cp38-none-win_amd64.whl

    cd TensorRT-8.x.x.x\uff
    pip install uff-0.6.9-py2.py3-none-any.whl

    cd TensorRT-8.x.x.x\onnx_graphsurgeon
    pip install onnx_graphsurgeon-0.3.12-py2.py3-none-any.whl

    cd TensorRT-8.x.x.x\graphsurgeon
    pip install graphsurgeon-0.4.6-py2.py3-none-any.whl
    ```

## 校验安装

```shell
>>import tensorrt as trt
>> trt.__version__
>> 8.4.5.1
```

# 2.导出engine模型

下载`yolov5-v6.1`版本源码，在虚拟环境中执行`pip install -r requirements.txt`安装依赖，然后执行`python export.py --weights yolov5s.pt --include engine --device 0`导出`engine`模型文件。


# 3.TensorRT的Python API

## 3.1.模型反序列化

```python
import tensorrt as trt
# 反序列化(加载)模型
logger = trt.Logger(trt.Logger.VERBOSE)
with open(model_path, 'rb') as f:
    model: trt.ICudaEngine = trt.Runtime(logger).deserialize_cuda_engine(f.read())
```

## 3.2.模型参数获取

```python
Binding = namedtuple("Binding", ('name', 'dtype', 'shape', 'data', 'ptr'))
binding = OrderedDict()
for index in range(model.num_bindings):
    name = model.get_binding_name(index)
    dtype = trt.nptype(model.get_binding_dtype(index))
    shape = model.get_binding_shape(index)
    data = torch.from_numpy(np.empty(shape, dtype=np.dtype(dtype))).to(device)

    binding[name] = Binding(name, dtype, shape, data, int(data.data_ptr()))

# 使用字典生成式，获取binding的key，和value对应的内存地址
binding_pointer = OrderedDict((key, value.ptr) for key, value in binding.items())
```

## 3.3.模型推理上下文构建

```python
# 创建指令执行上下文对象
context = model.create_execution_context()
```

## 3.4.数据预处理
    
```python
# 颜色通道转换
image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 处理图片尺寸
row, col, _ = image_np.shape
_max = max(col, row)
inputs = np.zeros((_max, _max, 3), np.uint8)
inputs[0:row, 0:col] = image_np

# 获取图片缩放比例
image_width, image_height, _ = inputs.shape
self.x_factor = image_width / self.image_size
self.y_factor = image_height / self.image_size

# 创建图片预处理工具
transformation = transforms.Compose([
    transforms.Resize((image_size, image_size)),
    transforms.ToTensor()
])

# 图片预处理
inputs = Image.fromarray(inputs)
inputs = self.transformation(inputs).to(self.device)
inputs = inputs.unsqueeze(0)
```

## 3.5.模型推理

```python
# inputs是输入数据，类型为torch.Tensor,shape为[1, 3, 640,640]
self.binding_pointer['images'] = inputs.data_ptr()
self.context.execute_v2(list(self.binding_pointer.values()))
# result是推理结果，由于运算在GPU上，需要将数据转移到CPU上
result = self.binding['output'].data.cpu().numpy()
```


## 3.6.推理结果后处理

由于推理结果存在大量重叠的`bbox`，需要进行`NMS`处理，后续根据每个`bbox`的置信度和用户设定的置信度阈值进行过滤，最终得到最终的`bbox`，和对应的类别、置信度。

### 3.6.1 NMS

`opencv-python`模块提供了`NMSBoxes`方法，用于进行`NMS`处理。

```python
cv2.dnn.NMSBoxes(bboxes, scores, score_threshold, nms_threshold, eta=None, top_k=None)
```

- `bboxes`: `bbox`列表，`shape`为`(N,4)`，`N`为`bbox`数量，`4`为`bbox`的`x,y,w,h`。
- `scores`: `bbox`对应的置信度列表，`shape`为`(N,1)`，`N`为`bbox`数量。
- `score_threshold`: 置信度阈值，小于该阈值的`bbox`将被过滤。
- `nms_threshold`: `NMS`阈值

`NMSBoxes`函数返回值为`bbox`索引列表，`shape`为`(M,)`，`M`为`bbox`数量.

### 3.6.2 score_threshold过滤

根据`NMS`处理后的`bbox`索引列表，过滤置信度小于`score_threshold`的`bbox`。

### 3.6.3 bbox坐标转换与还原

`YOLOv5`模型输出的`bbox`坐标为`cxcywh`格式，需要转换为`xyxy`格式，此外，由于之前对图片进行了`resize`操作，所以需要将`bbox`坐标还原到原始图片的尺寸。
转换方法如下：

```python
# 获取原始图片的尺寸(填充后)
image_width, image_height, _ = input_image.shape
# 计算缩放比
x_factor = image_width / INPUT_WIDTH  #  640
y_factor = image_height / INPUT_HEIGHT #  640 

# 将cxcywh坐标转换为xyxy坐标
x1 = int((x - w / 2) * x_factor)
y1 = int((y - h / 2) * y_factor)
w = int(w * x_factor)
h = int(h * y_factor)
x2 = x1 + w
y2 = y1 + h
```

`x1`,`y1`,`x2`,`y2`即为`bbox`的`xyxy`坐标。


# 4.示例代码

源代码一共有两份，其中一份是函数的拼接与调用，比较方便调试，另一份是封装成类，方便集成到其他项目中。

## 3.1 未封装
```python
import tensorrt as trt
from torchvision import transforms
import torch
from collections import OrderedDict, namedtuple
import cv2 as cv
import time
import numpy as np

img_transform = transforms.Compose([
    transforms.Resize((640, 640)),
    transforms.ToTensor()
])


def load_classes():
    with open("uav_bird.txt", "r") as f:
        class_list = [cname.strip() for cname in f.readlines()]
    return class_list


def format_yolov5(frame):
    row, col, _ = frame.shape
    _max = max(col, row)
    result = np.zeros((_max, _max, 3), np.uint8)
    result[0:row, 0:col] = frame
    result = cv.cvtColor(result, cv.COLOR_BGR2RGB)
    return result


def wrap_detection(input_image, output_data):
    class_ids = []
    confidences = []
    boxes = []
    # print(output_data.shape)
    rows = output_data.shape[0]

    image_width, image_height, _ = input_image.shape

    x_factor = image_width / 640.0
    y_factor = image_height / 640.0

    for r in range(rows):
        row = output_data[r]
        confidence = row[4]
        if confidence >= 0.4:

            classes_scores = row[5:]
            class_id = np.argmax(classes_scores)
            if (classes_scores[class_id] > .25):
                confidences.append(confidence)

                class_ids.append(class_id)

                x, y, w, h = row[0].item(), row[1].item(), row[2].item(), row[3].item()
                left = int((x - 0.5 * w) * x_factor)
                top = int((y - 0.5 * h) * y_factor)
                width = int(w * x_factor)
                height = int(h * y_factor)
                box = np.array([left, top, width, height])
                boxes.append(box)

    indexes = cv.dnn.NMSBoxes(boxes, confidences, 0.25, 0.45)

    result_class_ids = []
    result_confidences = []
    result_boxes = []

    for i in indexes:
        result_confidences.append(confidences[i])
        result_class_ids.append(class_ids[i])
        result_boxes.append(boxes[i])

    return result_class_ids, result_confidences, result_boxes


def gpu_trt_demo():
    class_list = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
                  "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                  "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
                  "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
                  "sports ball",
                  "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
                  "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
                  "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
                  "chair",
                  "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
                  "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
                  "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier",
                  "toothbrush"]
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    Binding = namedtuple('Binding', ('name', 'dtype', 'shape', 'data', 'ptr'))
    logger = trt.Logger(trt.Logger.INFO)
    with open("weights/yolov5s.engine", 'rb') as f, trt.Runtime(logger) as runtime:
        model = runtime.deserialize_cuda_engine(f.read())
    bindings = OrderedDict()
    for index in range(model.num_bindings):
        name = model.get_binding_name(index)
        dtype = trt.nptype(model.get_binding_dtype(index))
        shape = model.get_binding_shape(index)
        data = torch.from_numpy(np.empty(shape, dtype=np.dtype(dtype))).to(device)
        bindings[name] = Binding(name, dtype, shape, data, int(data.data_ptr()))
    binding_addrs = OrderedDict((n, d.ptr) for n, d in bindings.items())
    context = model.create_execution_context()

    capture = cv.VideoCapture(0)
    colors = [(255, 255, 0), (0, 255, 0), (0, 255, 255), (255, 0, 0)]
    while True:
        _, frame = capture.read()
        if frame is None:
            print("End of stream")
            break
        start = time.time()
        image = format_yolov5(frame)
        x_input = img_transform(image).view(1, 3, 640, 640).to(device) # (1,3,640,640)
        binding_addrs['images'] = int(x_input.data_ptr())
        context.execute_v2(list(binding_addrs.values()))
        out_prob = bindings['output'].data.cpu().numpy()
        end = time.time()

        class_ids, confidences, boxes = wrap_detection(image, np.squeeze(out_prob, 0))
        for (classid, confidence, box) in zip(class_ids, confidences, boxes):
            color = colors[int(classid) % len(colors)]
            cv.rectangle(frame, box, color, 2)
            cv.rectangle(frame, (box[0], box[1] - 20), (box[0] + box[2], box[1]), color, -1)
            cv.putText(frame, class_list[classid], (box[0], box[1] - 10), cv.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0))

        inf_end = end - start
        fps = 1 / inf_end
        fps_label = "FPS: %.2f" % fps
        cv.putText(frame, fps_label, (10, 25), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv.imshow("YOLOv5 + TensorRT8.4.x by gloomyfish", frame)
        if cv.waitKey(1) == ord('q'):
            break
    cv.destroyAllWindows()


if __name__ == "__main__":
    gpu_trt_demo()

```

## 3.2 封装成类调用

```python
from pathlib import Path
from collections import namedtuple, OrderedDict

import numpy as np
import cv2
from PIL import Image
from typing import List, Union
import torch
from torchvision import transforms

import tensorrt as trt


class YOLOv5TRTInference(object):
    def __init__(self,
                 model_path: str,
                 labels,
                 image_size=640,
                 score_threshold=0.45,
                 nms_threshold=0.4):
        assert Path(model_path).exists(), f"the model path not exists"
        # 检查运行设备
        device = torch.device("cuda:0") if torch.cuda.is_available() else torch.device("CPU")

        coco_class_names = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
                            "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                            "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
                            "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard",
                            "sports ball", "kite", "baseball bat", "baseball glove", "skateboard", "surfboard",
                            "tennis racket", "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana",
                            "apple", "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
                            "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
                            "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink", "refrigerator",
                            "book", "clock", "vase", "scissors", "teddy bear", "hair drier", "toothbrush"]
        if labels is None or len(labels) == 0:
            self.labels = coco_class_names
        else:
            self.labels = labels
        self.colors = np.random.uniform(0, 255, size=(len(self.labels), 3))

        self.x_factor = 1
        self.y_factor = 1
        self.xyxy = True

        # 创建图片预处理工具
        transformation = transforms.Compose([
            transforms.Resize((image_size, image_size)),
            transforms.ToTensor()
        ])

        # 反序列化(加载)模型
        logger = trt.Logger(trt.Logger.VERBOSE)
        with open(model_path, 'rb') as f:
            model: trt.ICudaEngine = trt.Runtime(logger).deserialize_cuda_engine(f.read())

        Binding = namedtuple("Binding", ('name', 'dtype', 'shape', 'data', 'ptr'))
        binding = OrderedDict()
        for index in range(model.num_bindings):
            name = model.get_binding_name(index)
            dtype = trt.nptype(model.get_binding_dtype(index))
            shape = model.get_binding_shape(index)
            data = torch.from_numpy(np.empty(shape, dtype=np.dtype(dtype))).to(device)

            binding[name] = Binding(name, dtype, shape, data, int(data.data_ptr()))

        # 使用字典生成式，获取binding的key，和value对应的内存地址
        binding_pointer = OrderedDict((key, value.ptr) for key, value in binding.items())

        # 创建指令执行上下文对象
        context = model.create_execution_context()

        self.__dict__.update(locals())

    def preprocess(self, image: np.ndarray):
        # 预处理图片
        image_np = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        row, col, _ = image_np.shape
        _max = max(col, row)
        inputs = np.zeros((_max, _max, 3), np.uint8)
        inputs[0:row, 0:col] = image_np
        image_width, image_height, _ = inputs.shape
        self.x_factor = image_width / self.image_size
        self.y_factor = image_height / self.image_size

        inputs = Image.fromarray(inputs)
        inputs = self.transformation(inputs).to(self.device)
        inputs = inputs.unsqueeze(0)
        return inputs

    def inference(self, inputs: np.ndarray) -> np.ndarray:
        self.binding_pointer['images'] = inputs.data_ptr()
        self.context.execute_v2(list(self.binding_pointer.values()))
        result = self.binding['output'].data.cpu().numpy()
        return result[0]

    def wrap_detection(self, result: np.ndarray, to_xyxy: bool = True) -> (List[int], List[float], List[List[int]]):

        # using NMS algorithm to filter out the overlapping bounding boxes
        indices = cv2.dnn.NMSBoxes(result[:, 0:4].tolist(), result[:, 4].tolist(), self.score_threshold,
                                   self.nms_threshold)
        # get the real data after filtering
        result = result[indices]

        # filter the bounding boxes with confidence lower than the threshold
        result = result[result[:, 4] > self.score_threshold]

        bounding_boxes, confidences, classes = [], [], []
        for item in result:
            box = item[0:4]
            confidence = float(item[4])
            class_prediction_probability = item[5:]
            most_probable_class_index = np.argmax(class_prediction_probability)
            #
            x, y, w, h = box
            left = int((x - 0.5 * w) * self.x_factor)
            top = int((y - 0.5 * h) * self.y_factor)
            width = int(w * self.x_factor)
            height = int(h * self.y_factor)

            if to_xyxy:
                self.xyxy = True
                bounding_box = [left, top, left + width, top + height]
            else:
                self.xyxy = False
                bounding_box = [left, top, width, height]

            bounding_boxes.append(bounding_box)
            confidences.append(confidence)
            classes.append(most_probable_class_index)

        return classes, confidences, bounding_boxes

    def detect(self, image: Union[str, np.ndarray], visualize=True) -> np.ndarray:
        if isinstance(image, str):
            image = cv2.imread(image)
        inputs = self.preprocess(image)
        result = self.inference(inputs)
        class_ids, confidences, boxes = self.wrap_detection(result, to_xyxy=True)

        if visualize:
            for (class_id, confidence, box) in zip(class_ids, confidences, boxes):
                color = self.colors[int(class_id) % len(self.colors)]
                label = self.coco_class_names[int(class_id)]
                if self.xyxy:
                    cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), color, 2)
                else:
                    cv2.rectangle(image, box, color, 2)

                cv2.rectangle(image, (box[0], box[1] - 20), (box[0] + 100, box[1]), color, -1)
                cv2.putText(image, str(label), (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        return image


def detect_image(image_path, detector):
    result = detector.detect(image_path)
    cv2.imshow('show', result)
    cv2.waitKey(0)


if __name__ == '__main__':
    # 设置模型路径
    model_path = 'weights/yolov5s.engine'

    image_path = 'data/images/zidane.jpg'

    detector = YOLOv5TRTInference(model_path, None)

    detect_image(image_path, detector)
    exit(0)
```
