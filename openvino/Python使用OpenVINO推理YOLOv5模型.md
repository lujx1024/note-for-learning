
# 概述

本文档主要描述`python`平台，使用`openvino`模块推理`YOLOv5`导出`IR`模型的方法。

文档主要包含以下内容：

- `openvino`模块的安装
- 模型格式的说明
- openvino的基础API接口，包括`初始化`，`模型加载`，`模型参数获取`，`模型推理`等
- 图片数据的预处理
- 推理结果后处理，包括`NMS`,`cxcywh`坐标转换为`xyxy`坐标等
- 关键方法的调用与参数说明
- 完整的示例代码

# 1.环境部署

## 预安装环境

1. `(Windows) Visual Studio 2019`
2. `Anaconda3` 或 `MiniConda3`

> 注: 使用`openvino`需确认`CPU`型号是`Intel`的，否则无法使用。

## `openvino`安装

- `pytorch 1.7.1+cu110`
- `onnxruntime-gpu 1.7.0`

```bash
conda create -n openvino python=3.8 -y

conda activate ort

pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html

pip install onnxruntime-gpu==1.7.0
```

## ONNX模型转换

可通过官方链接下载YOLOv5的官方预训练模型，模型格式为`pt`.[下载链接](https://github.com/ultralytics/yolov5/releases/download/v6.1/yolov5s.pt)
`YOLOv5`官方项目提供了`pt`格式模型转换为`ONNX`格式模型的脚本，[项目链接](https://github.com/ultralytics/yolov5)

模型导出指令：

```bash
python export --weights yolov5s.pt --include openvino
```
> 注：导出文件执行指令所需环境安装配置参考官方项目`README`文档即可，不在赘述。

指令执行完成后，会在`yolov5s.pt`同级目录下生成名为`yolov5s_openvino_model`的文件夹，文件夹内包含`IR`模型文件。文件结构如下：

```bash
yolov5s_openvino_model
├── yolov5s.bin
├── yolov5s.mapping
└── yolov5s.xml
```

# 2.OpenVINO基础API

## 2.1 初始化

```python
from openvino.runtime import Core
core = Core()
```

## 2.2 获取设备信息

```python
devices = core.available_devices

for device in devices:
    device_name = core.get_property(device, "FULL_DEVICE_NAME")
    print(f"{device}: {device_name}")
```

代码输出示例:

```text
device_name: 12th Gen Intel(R) Core(TM) i5-12400F
device_name: NVIDIA GeForce RTX 2060 SUPER (dGPU)
```

## 2.3 加载模型

加载`OpenVINO` 中间表示(`IR`)模型文件，返回`ExecutableNetwork`对象。

```python
# load the openvino IR model
yolo_model_path = "weights/yolov5s_openvino_model/yolov5s.xml"
model = core.read_model(model=yolo_model_path)
compiled_model = core.compile_model(model=model, device_name="AUTO")
```

## 2.4 获取模型输入输出信息

```python
# 获取输入层信息
input_layer = model.inputs[0]
print(f"input_layer: {input_layer}")

# 获取输出层信息
output_layer = model.outputs
print(f"output_layer: {output_layer}")
```

代码输出示例:

```text
input_layer: <Output: names[images] shape[1,3,640,640] type: f32>
output_layer: [<Output: names[output] shape[1,25200,85] type: f32>, <Output: names[345] shape[1,3,80,80,85] type: f32>, <Output: names[403] shape[1,3,40,40,85] type: f32>, <Output: names[461] shape[1,3,20,20,85] type: f32>]
```

可以看出，模型仅有一个输入层，但是有4个输出层，符合`YOLOv5`模型的多层输出特性。
在推理过程中，我们只需要关注`output`这个输出层就好了。

更进一步，为了后续的模型推理的预处理和后处理，我们需要获取模型的输入输出层的相关信息，包括：

- 输入层的name、shape、type
- 输出层对应的name、shape、type

```python
# 如果输入层只有一层，直接调用any_name获取输入层名称
input_name = input_layer.any_name
print(f"input_name: {input_name}")
N, C, H, W = input_layer.shape
print(f"N: {N}, C: {C}, H: {H}, W: {W}")
input_dtype = input_layer.element_type
print(f"input_dtype: {input_dtype}")

output_name = output_layer[0].any_name
print(f"output_name: {output_name}")
output_shape = output_layer[0].shape
print(f"output_shape: {output_shape}")
output_dtype = output_layer[0].element_type
print(f"output_dtype: {output_dtype}")
```
输出示例:

```text
input_name: images
N: 1, C: 3, H: 640, W: 640
input_dtype: <Type: 'float32'>
output_name: output
output_shape: [1,25200,85]
output_dtype: <Type: 'float32'>
```

## 2.5 模型推理

```python
image = cv2.imread(str(image_filename))
# image.shape = (height, width, channels)

# N,C,H,W = batch size, number of channels, height, width.
N, C, H, W = input_layer.shape
# OpenCV resize expects the destination size as (width, height).
resized_image = cv2.resize(src=image, dsize=(W, H))
# resized_image.shape = (height, width, channels)

input_data = np.expand_dims(np.transpose(resized_image, (2, 0, 1)), 0).astype(np.float32)
# input_data.shape = (N, C, H, W)

# for single input models only
result = compiled_model(input_data)[output_layer]

# for multiple inputs in a list
result = compiled_model([input_data])[output_layer]

# or using a dictionary, where the key is input tensor name or index
result = compiled_model({input_layer.any_name: input_data})[output_layer]
```

# 3.关键代码

## 2.1 图片数据预处理

数据预处理步骤包括resize，归一化，颜色通道转换，NCWH维度转换等。

`resize`之前，有一个非常常用的trick来处理非方形的图片，即计算图形的最长边，以此最长边为基础，创建一个正方形，并将原图形放置到左上角，剩余部分用黑色填充，这样做的好处是，不会改变原图形的长宽比，同时也不会改变原图形的内容。

```python
 # image preprocessing, the trick is to make the frame to be a square but not twist the image
row, col, _ = frame.shape  # get the row and column of the origin frame array
_max = max(row, col)  # get the max value of row and column
input_image = np.zeros((_max, _max, 3), dtype=np.uint8)  # create a new array with the max value
input_image[:row, :col, :] = frame  # paste the original frame  to make the input_image to be a square
```

完成图片的填充后,继续执行resize，归一化，颜色通道转换等操作。

```python
blob = cv2.dnn.blobFromImage(image, scalefactor=1 / 255.0, size=(640,640), swapRB=True, crop=False)
```
- `image`: 输入图片数据,`numpy.ndarray`格式,`shape`为`(H,W,C)`,Channel顺序为`BGR`。
- `scalefactor`: 图片数据归一化系数，一般为`1/255.0`。
- `size`: 图片resize尺寸，以模型的输入要求为准，这里是`(640,640)`。
- `swapRB`: 是否交换颜色通道，即转换`BGR`为`RGB` `True`表示交换，`False`表示不交换，由于`opencv`读取图片数据的颜色通道顺序为`BGR`，而`YOLOv5`模型的输入要求为`RGB`，所以这里需要交换颜色通道。
- `crop`: 是否裁剪图片，`False`表示不裁剪。

`blobFromImage`函数返回四维Mat对象(NCHW dimensions order),数据的shape为`(1,3,640,640)`


## 2.4 推理结果后处理

由于推理结果存在大量重叠的`bbox`，需要进行`NMS`处理，后续根据每个`bbox`的置信度和用户设定的置信度阈值进行过滤，最终得到最终的`bbox`，和对应的类别、置信度。

### 2.4.1 NMS

`opencv-python`模块提供了`NMSBoxes`方法，用于进行`NMS`处理。

```python
cv2.dnn.NMSBoxes(bboxes, scores, score_threshold, nms_threshold, eta=None, top_k=None)
```

- `bboxes`: `bbox`列表，`shape`为`(N,4)`，`N`为`bbox`数量，`4`为`bbox`的`x,y,w,h`。
- `scores`: `bbox`对应的置信度列表，`shape`为`(N,1)`，`N`为`bbox`数量。
- `score_threshold`: 置信度阈值，小于该阈值的`bbox`将被过滤。
- `nms_threshold`: `NMS`阈值

`NMSBoxes`函数返回值为`bbox`索引列表，`shape`为`(M,)`，`M`为`bbox`数量.

### 2.4.2 score_threshold过滤

根据`NMS`处理后的`bbox`索引列表，过滤置信度小于`score_threshold`的`bbox`。

### 2.4.3 bbox坐标转换与还原

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
"""

this file is to demonstrate how to use openvino to do inference with yolov5 model exported from onnx to openvino format
"""

from typing import List

import cv2
import numpy as np
import time
from pathlib import Path
from openvino.runtime import Core


def build_model(model_path: str) -> cv2.dnn_Net:
    """
    build the model with opencv dnn module
    Args:
        model_path: the path of the model, the model should be in onnx format

    Returns:
        the model object
    """
    # load the model
    core = Core()
    model = core.read_model(model_path)
    for device in core.available_devices:
        print(device)
    compiled_model = core.compile_model(model=model, device_name="AUTO")
    # output_layer = compiled_model.output(0)
    return compiled_model


def inference(image: np.ndarray, model: cv2.dnn_Net) -> np.ndarray:
    """
    inference the model with the input image
    Args:
        image: the input image in numpy array format, the shape should be (height, width, channel),
        the color channels should be in GBR order, like the original opencv image format
        model: the model object

    Returns:
        the output data of the model, the shape should be (1, 25200, nc+5), nc is the number of classes
    """
    # image preprocessing, include resize, normalization, channel swap like BGR to RGB, and convert to blob format
    # get a 4-dimensional Mat with NCHW dimensions order.
    blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (INPUT_WIDTH, INPUT_HEIGHT), swapRB=True, crop=False)

    output_layer = model.output(0)
    outs = model([blob])[output_layer]


    start = time.perf_counter()
    # inference
    # outs = model.forward()

    end = time.perf_counter()

    # print("inference time: ", end - start)

    # the shape of the output data is (1, 25200, nc+5), nc is the number of classes
    return outs


def xywh_to_xyxy(bbox_xywh, image_width, image_height):
    """
    Convert bounding box coordinates from (center_x, center_y, width, height) to (x_min, y_min, x_max, y_max) format.

    Parameters:
        bbox_xywh (list or tuple): Bounding box coordinates in (center_x, center_y, width, height) format.
        image_width (int): Width of the image.
        image_height (int): Height of the image.

    Returns:
        tuple: Bounding box coordinates in (x_min, y_min, x_max, y_max) format.
    """
    center_x, center_y, width, height = bbox_xywh
    x_min = max(0, int(center_x - width / 2))
    y_min = max(0, int(center_y - height / 2))
    x_max = min(image_width - 1, int(center_x + width / 2))
    y_max = min(image_height - 1, int(center_y + height / 2))
    return x_min, y_min, x_max, y_max


def wrap_detection(
        input_image: np.ndarray,
        output_data: np.ndarray,
        labels: List[str],
        confidence_threshold: float = 0.6
) -> (List[int], List[float], List[List[int]]):
    # the shape of the output_data is (25200,5+nc),
    # the first 5 elements are [x, y, w, h, confidence], the rest are prediction scores of each class

    image_width, image_height, _ = input_image.shape
    x_factor = image_width / INPUT_WIDTH
    y_factor = image_height / INPUT_HEIGHT

    # transform the output_data[:, 0:4] from (x, y, w, h) to (x_min, y_min, x_max, y_max)
    # output_data[:, 0:4] = np.apply_along_axis(xywh_to_xyxy, 1, output_data[:, 0:4], image_width, image_height)

    indices = cv2.dnn.NMSBoxes(output_data[:, 0:4].tolist(), output_data[:, 4].tolist(), 0.6, 0.4)

    # print(indices)
    raw_boxes = output_data[:, 0:4][indices]
    raw_confidences = output_data[:, 4][indices]
    raw_class_prediction_probabilities = output_data[:, 5:][indices]

    criteria = raw_confidences > confidence_threshold
    raw_class_prediction_probabilities = raw_class_prediction_probabilities[criteria]
    raw_boxes = raw_boxes[criteria]
    raw_confidences = raw_confidences[criteria]

    bounding_boxes, confidences, class_ids = [], [], []
    for class_prediction_probability, box, confidence in zip(raw_class_prediction_probabilities, raw_boxes,
                                                             raw_confidences):
        # find the least and most probable classes' indices and their probabilities
        # min_val, max_val, min_loc, mac_loc = cv2.minMaxLoc(class_prediction_probability)
        most_probable_class_index = np.argmax(class_prediction_probability)
        label = labels[most_probable_class_index]
        confidence = float(confidence)


        x, y, w, h = box
        left = int((x - 0.5 * w) * x_factor)
        top = int((y - 0.5 * h) * y_factor)
        width = int(w * x_factor)
        height = int(h * y_factor)
        bounding_box = [left, top, width, height]
        bounding_boxes.append(bounding_box)
        confidences.append(confidence)
        class_ids.append(most_probable_class_index)

    return class_ids, confidences, bounding_boxes


coco_class_names = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
                    "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                    "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
                    "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball",
                    "kite", "baseball bat", "baseball glove", "skateboard", "surfboard", "tennis racket",
                    "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
                    "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake", "chair",
                    "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop", "mouse",
                    "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
                    "refrigerator", "book", "clock", "vase", "scissors", "teddy bear", "hair drier",
                    "toothbrush"]
# generate different colors for coco classes
colors = np.random.uniform(0, 255, size=(len(coco_class_names), 3))

INPUT_WIDTH = 640
INPUT_HEIGHT = 640
CONFIDENCE_THRESHOLD = 0.7
NMS_THRESHOLD = 0.45


def video_detector(video_src):
    cap = cv2.VideoCapture(video_src)

    # 3. inference and show the result in a loop
    while cap.isOpened():
        success, frame = cap.read()
        start = time.perf_counter()
        if not success:
            break

        # image preprocessing, the trick is to make the frame to be a square but not twist the image
        row, col, _ = frame.shape  # get the row and column of the origin frame array
        _max = max(row, col)  # get the max value of row and column
        input_image = np.zeros((_max, _max, 3), dtype=np.uint8)  # create a new array with the max value
        input_image[:row, :col, :] = frame  # paste the original frame  to make the input_image to be a square

        # inference
        output_data = inference(input_image, net)  # the shape of output_data is (1, 25200, 85)

        # define coco dataset class names dictionary

        # 4. wrap the detection result
        class_ids, confidences, boxes = wrap_detection(input_image, output_data[0], coco_class_names)

        # wrap_detection(input_image, output_data[0], coco_class_names) ##

        # 5. draw the detection result on the frame
        for (class_id, confidence, box) in zip(class_ids, confidences, boxes):
            color = colors[int(class_id) % len(colors)]
            label = coco_class_names[int(class_id)]

            # cv2.rectangle(frame, box, color, 2)

            # print(type(box), box[0], box[1], box[2], box[3], box)
            xmin, ymin, width, height = box
            cv2.rectangle(frame, (xmin, ymin), (xmin + width, ymin + height), color, 2)
            # cv2.rectangle(frame, box, color, 2)
            # cv2.rectangle(frame, [box[0], box[1], box[2], box[3]], color, thickness=2)

            # cv2.rectangle(frame, (box[0], box[1] - 20), (box[0] + 100, box[1]), color, -1)
            cv2.putText(frame, str(label), (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        finish = time.perf_counter()
        FPS = round(1.0 / (finish - start), 2)
        cv2.putText(frame, str(FPS), (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        # 6. show the frame
        cv2.imshow("frame", frame)

        # 7. press 'q' to exit
        if cv2.waitKey(1) == ord('q'):
            break

    # 8. release the capture and destroy all windows
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # there are 4 steps to use opencv dnn module to inference onnx model exported by yolov5 and show the result

    # 1. load the model
    model_path = Path("weights/yolov5s_openvino_model/yolov5s.xml")
    # model_path = Path("weights/POT_INT8_openvino_model/yolov5s_int8.xml")
    net = build_model(str(model_path))
    # 2. load the video capture
    video_source = 0
    # video_source = 'rtsp://admin:aoto12345@192.168.8.204:554/h264/ch1/main/av_stream'
    video_detector(video_source)

    exit(0)
```

## 3.2 封装成类调用

```python
import cv2
import numpy as np
from pathlib import Path
import time
from typing import List
from glob import glob
from openvino.runtime import Core


class YoloV5OpenvinoInference:
    def __init__(self, model_path: str,
                 imgsize: int = 640,
                 labels: List[str] = None,
                 score_threshold: float = 0.6,
                 nms_threshold: float = 0.45):
        self.load_model(model_path)
        self.imgsize = imgsize
        self.score_threshold = score_threshold
        self.nms_threshold = nms_threshold
        self.coco_class_names = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
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
        if labels is None or len(labels) == 0:
            self.labels = self.coco_class_names
        else:
            self.labels = labels
        self.colors = np.random.uniform(0, 255, size=(len(self.labels), 3))

        self.x_factor = 1
        self.y_factor = 1
        self.xyxy = True

    def load_model(self, model_path: str) -> None:

        if not Path(model_path).exists():
            raise FileNotFoundError(f"model file {model_path} not found")
        self.core = Core()
        self.loaded_model = self.core.read_model(model_path)
        self.compiled_model = self.core.compile_model(model=self.loaded_model, device_name="AUTO")
        self.output_layer = self.loaded_model.output(0)

    def preprocess(self, image: np.ndarray) -> np.ndarray:
        row, col, _ = image.shape
        _max = max(row, col)
        input_image = np.zeros((_max, _max, 3), dtype=np.uint8)
        input_image[:row, :col, :] = image
        image_width, image_height, _ = input_image.shape
        self.x_factor = image_width / self.imgsize
        self.y_factor = image_height / self.imgsize
        return input_image

    def inference(self, image: np.ndarray) -> np.ndarray:
        image = self.preprocess(image)
        blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (self.imgsize, self.imgsize), swapRB=True, crop=False)
        start = time.perf_counter()
        outs = self.compiled_model([blob])

        # TODO
        # 此处由于model.output(0)返回和推理输出的数据类型可能不一致(openvino.runtime.ConstOutput和openvino.runtime.Output)
        # 导致取出输出层数据报错，暂时先这样处理
        output_layer = [item for item in outs if item.any_name == "output"][0]
        outs = outs[output_layer]
        # outs = self.compiled_model([blob])['output']
        end = time.perf_counter()
        print("inference time: ", end - start)
        return outs[0]

    def wrap_detection(self, result: np.ndarray, to_xyxy: bool = True) -> (List[int], List[float], List[List[int]]):

        # using NMS algorithm to filter out the overlapping bounding boxes
        indices = cv2.dnn.NMSBoxes(result[:, 0:4].tolist(), result[:, 4].tolist(), 0.6, 0.4)
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

    def detect(self, image: np.ndarray, visualize=True) -> np.ndarray:
        img = self.preprocess(image)
        result = self.inference(img)
        class_ids, confidences, boxes = self.wrap_detection(result, to_xyxy=True)

        if visualize:
            for (class_id, confidence, box) in zip(class_ids, confidences, boxes):
                color = yolo_v5.colors[int(class_id) % len(yolo_v5.colors)]
                label = yolo_v5.coco_class_names[int(class_id)]
                if self.xyxy:
                    cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), color, 2)
                else:
                    cv2.rectangle(image, box, color, 2)

                cv2.rectangle(image, (box[0], box[1] - 20), (box[0] + 100, box[1]), color, -1)
                cv2.putText(image, str(label), (box[0], box[1] - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        return image


def video_detector(video_src):
    cap = cv2.VideoCapture(video_src)

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            break

        frame = yolo_v5.detect(frame)
        cv2.imshow("frame", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def image_detector(image_src):
    image = cv2.imread(image_src)
    image = yolo_v5.detect(image)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    model_path = "weights/yolov5s_openvino_model/yolov5s.xml"
    yolo_v5 = YoloV5OpenvinoInference(model_path=model_path)

    video_source = 0
    # video_source = 'rtsp://admin:aoto12345@192.168.8.204:554/h264/ch1/main/av_stream'
    video_detector(video_source)

    # image_path = "data/images/bus.jpg"
    # image_detector(image_path)
    exit(0)
```

# 参考链接

- [OpenVINO官方API文档](https://docs.openvino.ai/2023.0/api/ie_python_api)
- [OpenVINO官方github示例](https://github.com/openvinotoolkit/openvino_notebooks/tree/main/notebooks)