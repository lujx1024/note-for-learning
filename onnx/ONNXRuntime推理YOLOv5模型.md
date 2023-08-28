[TOC]

# 概述

本文档主要描述`python`平台，使用`onnxruntime`推理`YOLOv5`模型的方法。


文档主要包含以下内容：

- `onnxruntime-gpu`模块和`pytorch`的安装
- `YOLOv5`模型格式的说明
- `ONNX`格式模型的加载
- 图片数据的预处理
- 模型推理
- 推理结果后处理，包括`NMS`,`cxcywh`坐标转换为`xyxy`坐标等
- 关键方法的调用与参数说明
- 完整的示例代码

# 1.环境部署

## 预安装环境
1. `(Windows) Visual Studio 2019`
2. `CUDA 10.2` `CUDNN 7.6.5`
3. `Anaconda3` 或 `MiniConda3`


## `Pytorch`和`onnxruntime-gpu`安装

- `pytorch 1.7.1+cu110`
- `onnxruntime-gpu 1.7.0`

```bash
conda create -n onnx python=3.8 -y

conda activate onnx

pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html

pip install onnxruntime-gpu==1.7.0
```

## ONNX模型转换

可通过官方链接下载YOLOv5的官方预训练模型，模型格式为`pt`.[下载链接](https://github.com/ultralytics/yolov5/releases/download/v6.1/yolov5s.pt)
`YOLOv5`官方项目提供了`pt`格式模型转换为`ONNX`格式模型的脚本，[项目链接](https://github.com/ultralytics/yolov5)

模型导出指令：

```bash
python export --weights yolov5s.pt --include onnx
```
> 注：导出文件执行指令所需环境安装配置参考官方项目`README`文档即可，不在赘述。


# 2.关键代码

## 2.1 Session创建

`opencv-python`模块提供了`readNetFromONNX`方法，用于加载`ONNX`格式模型。


```python
import onnx
import onnxruntime as ort
model_path = "weights/yolov5s.onnx"
onnx_model = onnx.load(model_path)
onnx.checker.check_model(onnx_model)
session = ort.InferenceSession(model_path, providers=['CUDAExecutionProvider', "CPUExecutionProvider"])

```

## 2.2 图片数据预处理

数据预处理步骤包括resize，归一化，颜色通道转换，NCWH维度转换等,这里使用`torchvision.transforms`模块提供的方法进行图片预处理。

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
trans = transforms.Compose([
        transforms.Resize((640, 640)),
        transforms.ToTensor()
    ])
input_image = trans(Image.fromarray(input_image))
input_image = input_image.unsqueeze(0)
```

- `transforms.Resize`: 图片resize尺寸，以模型的输入要求为准，这里是`(640,640)`
- `transforms.ToTensor()`: 转换图片数据为张量数据,并进行`transpose`操作,输出数据格式为`(C,H,W)`
- `unsqueeze(0)`: 输入数据升级维度，输出格式为`(1,C,H,W)`

## 2.3 推理

```python
ort_inputs = {session.get_inputs()[0].name: inputs.numpy()}
ort_outs = session.run(None, ort_inputs)
```
`ort_out`输出格式为`list`,`shape`为`[(1,25200,5+nc),]`

## 2.4 模型输出数据后处理

由于推理结果存在大量重叠的`bbox`，需要进行`NMS`处理，后续根据每个`bbox`的置信度和用户设定的置信度阈值进行过滤，最终得到最终的`bbox`，和对应的类别、置信度。

### 2.4.2 score_threshold过滤

根据`NMS`处理后的`bbox`索引列表，过滤置信度小于`score_threshold`的`bbox`。

```python
 # step 5. postprocessing
scores = out_prob[:, 4]  # Confidence scores are in the 5th column (0-indexed)
class_ids = out_prob[:, 5:].argmax(axis=1)  # Class labels are from the 6th column onwards
bounding_boxes_xywh = out_prob[:, :4]  # Bounding boxes in cxcywh format

# Filter out boxes based on confidence threshold
confidence_threshold = 0.7
mask = scores >= confidence_threshold
class_ids = class_ids[mask]
bounding_boxes_xywh = bounding_boxes_xywh[mask]
scores = scores[mask]
```

### 2.4.2 NMS

此处的`NMS`算法使用`torchvision.ops`提供的`nms`方法，查阅官方文档可知，使用`nms`函数需要传入`xyxy`格式的`boxes`，置信度阈值和`IOU`阈值,此前模型返回的数据中，box的坐标格式为`cxcywh`,因此调用`nms`之前，需要先做两步数据处理:

1. 转换`box`格式，从`cxcywh`到`xyxy`
2. 将所有输入参数转换为`Tensor`


> 注: 源码与官方文档
> torchvision.ops.nms(boxes: Tensor, scores: Tensor, iou_threshold: float) → Tensor[SOURCE]
```
Performs non-maximum suppression (NMS) on the boxes according to their intersection-over-union (IoU).

NMS iteratively removes lower scoring boxes which have an IoU greater than iou_threshold with another (higher scoring) box.

If multiple boxes have the exact same score and satisfy the IoU criterion with respect to a reference box, the selected box is not guaranteed to be the same between CPU and GPU. This is similar to the behavior of argsort in PyTorch when repeated values are present.

Parameters:
    boxes (Tensor[N, 4])) – boxes to perform NMS on. They are expected to be in (x1, y1, x2, y2) format with 0 <= x1 < x2 and 0 <= y1 < y2.

    scores (Tensor[N]) – scores for each one of the boxes

    iou_threshold (float) – discards all overlapping boxes with IoU > iou_threshold

Returns:
    int64 tensor with the indices of the elements that have been kept by NMS, sorted in decreasing order of scores

Return type:
    Tensor
```

### 2.4.3 bbox坐标转换与还原

`YOLOv5`模型输出的`bbox`坐标为`cxcywh`格式，需要转换为`xyxy`格式，NMS已经执行了此操作，由于之前对图片进行了`resize`操作，所以需要将`bbox`坐标还原到原始图片的尺寸。
转换方法如下：

```python
# 获取原始图片的尺寸(填充后)
image_width, image_height, _ = input_image.shape
# 计算缩放比
x_factor = image_width / INPUT_WIDTH  #  640
y_factor = image_height / INPUT_HEIGHT #  640 

# 还原原始尺寸
box[0] *= self.x_factor
box[1] *= self.y_factor
box[2] *= self.x_factor
box[3] *= self.y_factor
```

`box[0]`,`box[1]`,`box[2]`,`box[3]`即为`bbox`的`xyxy`坐标。

# 3. 示例代码(可运行)

源代码一共有两份，其中一份是函数的拼接与调用，比较方便调试，另一份是封装成类，方便集成到其他项目中。

## 3.1 未封装
```python
from typing import List

import onnx
from torchvision import transforms

from torchvision.ops import nms, box_convert
import cv2
import time
import numpy as np
import onnxruntime as ort
import torch
from PIL import Image

INPUT_WIDTH = 640
INPUT_HEIGHT = 640

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

colors = np.random.uniform(0, 255, size=(len(coco_class_names), 3))

if __name__ == '__main__':
    # step 1. Load the model
    model_path = "weights/yolov5s.onnx"
    onnx_model = onnx.load(model_path)
    onnx.checker.check_model(onnx_model)
    session = ort.InferenceSession(model_path, providers=['CUDAExecutionProvider', "CPUExecutionProvider"])

    capture = cv2.VideoCapture(0)

    # step 2. define the transform operation
    trans = transforms.Compose([
        transforms.Resize((640, 640)),
        transforms.ToTensor()
    ])

    while capture.isOpened():
        success, frame = capture.read()
        start = time.perf_counter()
        if not success:
            break

        # step 3. Image Preprocessing
        rows, cols, channels = frame.shape
        max_size = max(rows, cols)
        input_image = np.zeros((max_size, max_size, 3), dtype=np.uint8)
        input_image[:rows, :cols, :] = frame
        input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)
        inputs = trans(Image.fromarray(input_image))
        inputs = inputs.unsqueeze(0)
        if torch.cuda.is_available():
            inputs.to('cuda')
        # step 4. inference
        ort_inputs = {session.get_inputs()[0].name: inputs.numpy()}
        ort_outs = session.run(None, ort_inputs)
        out_prob = ort_outs[0][0]

        # step 5. postprocessing
        scores = out_prob[:, 4]  # Confidence scores are in the 5th column (0-indexed)
        class_ids = out_prob[:, 5:].argmax(axis=1)  # Class labels are from the 6th column onwards
        bounding_boxes_xywh = out_prob[:, :4]  # Bounding boxes in cxcywh format

        # Filter out boxes based on confidence threshold
        confidence_threshold = 0.7
        mask = scores >= confidence_threshold
        class_ids = class_ids[mask]
        bounding_boxes_xywh = bounding_boxes_xywh[mask]
        scores = scores[mask]

        bounding_boxes_xywh = torch.tensor(bounding_boxes_xywh, dtype=torch.float32)
        # Convert bounding boxes from xywh to xyxy format
        bounding_boxes_xyxy = box_convert(bounding_boxes_xywh, in_fmt='cxcywh', out_fmt='xyxy')

        # Perform Non-Maximum Suppression to filter candidate boxes
        scores = torch.tensor(scores, dtype=torch.float32)
        if torch.cuda.is_available():
            bounding_boxes_xyxy.to('cuda')
            scores.to('cuda')
        nms_start = time.perf_counter()
        keep_indices = nms(bounding_boxes_xyxy, scores, 0.4)
        nms_end = time.perf_counter()
        print(f"NMS took {nms_end - nms_start} seconds")
        class_ids = class_ids[keep_indices]
        confidences = scores[keep_indices]
        bounding_boxes = bounding_boxes_xyxy[keep_indices]

        for i in range(len(keep_indices)):
            try:
                class_id = class_ids[i]
            except IndexError as e:
                class_id = int(class_ids)
            confidence = confidences[i]
            box = bounding_boxes[i]
            color = colors[int(class_id) % len(colors)]
            label = coco_class_names[int(class_id)]

            # step 6. draw the bounding box
            xmin, ymin, xmax, ymax = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)

            cv2.rectangle(frame, (xmin, ymin - 20), (xmin + 100, ymin), color, -1)
            cv2.putText(frame, str(label), (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        finish = time.perf_counter()
        FPS = round(1.0 / (finish - start), 2)
        cv2.putText(frame, f"FPS: {str(FPS)}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        cv2.imshow("frame", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

    exit(0)

```

## 3.2 封装成类调用

```python
from typing import List
import numpy as np
import cv2
from torchvision import transforms
from torchvision.ops import nms, box_convert
from PIL import Image
import torch
import time
import onnxruntime as ort


class YoloV5ORTInference:
    def __init__(self, model_path: str,
                 imgsize: int = 640,
                 labels: List[str] = None,
                 score_threshold: float = 0.7,
                 nms_threshold: float = 0.45):
        self.session = self.build_session(model_path)
        self.imgsize = imgsize
        self.score_threshold = score_threshold
        self.nms_threshold = nms_threshold
        self.coco_class_names = ["person", "bicycle", "car", "motorcycle", "airplane", "bus", "train", "truck", "boat",
                                 "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
                                 "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack",
                                 "umbrella", "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard","sports ball",
                                 "kite", "baseball bat", "baseball glove", "skateboard", "surfboard","tennis racket",
                                 "bottle", "wine glass", "cup", "fork", "knife", "spoon", "bowl", "banana", "apple",
                                 "sandwich", "orange", "broccoli", "carrot", "hot dog", "pizza", "donut", "cake",
                                 "chair", "couch", "potted plant", "bed", "dining table", "toilet", "tv", "laptop",
                                 "mouse",  "remote", "keyboard", "cell phone", "microwave", "oven", "toaster", "sink",
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

    def build_session(self, model_path: str):
        session = ort.InferenceSession(model_path, providers=['CUDAExecutionProvider', "CPUExecutionProvider"])
        return session

    def preprocess(self, image):
        row, col, _ = image.shape
        _max = max(row, col)
        input_image = np.zeros((_max, _max, 3), dtype=np.uint8)
        input_image[:row, :col, :] = image
        image_width, image_height, _ = input_image.shape
        self.x_factor = image_width / self.imgsize
        self.y_factor = image_height / self.imgsize

        trans = transforms.Compose([
            transforms.Resize((self.imgsize, self.imgsize)),
            transforms.ToTensor()])

        input_image = cv2.resize(input_image, (self.imgsize, self.imgsize))
        input_image = trans(Image.fromarray(input_image))
        input_image = input_image.unsqueeze(0)

        if torch.cuda.is_available():
            input_image.to('cuda')

        return input_image

    def inference(self, inputs):
        ort_inputs = {self.session.get_inputs()[0].name: inputs.numpy()}
        ort_outs = self.session.run(None, ort_inputs)  # list[(1,25200,5+nc)], nc is the number of classes

        # TODO return only one picture's result, not batch
        return ort_outs[0][0]

    def postprocess(self, outputs, score_threshold, nms_threshold=0.4):
        scores = outputs[:, 4]  # Confidence scores are in the 5th column (0-indexed)
        class_ids = outputs[:, 5:].argmax(axis=1)  # Class labels are from the 6th column onwards
        bounding_boxes_xywh = outputs[:, :4]  # Bounding boxes in cxcywh format

        # Filter out boxes based on confidence threshold
        confidence_threshold = 0.7
        mask = scores >= confidence_threshold
        class_ids = class_ids[mask]
        bounding_boxes_xywh = bounding_boxes_xywh[mask]
        scores = scores[mask]

        bounding_boxes_xywh = torch.tensor(bounding_boxes_xywh, dtype=torch.float32)

        # Convert bounding boxes from xywh to xyxy format
        bounding_boxes_xyxy = box_convert(bounding_boxes_xywh, in_fmt='cxcywh', out_fmt='xyxy')

        # Perform Non-Maximum Suppression to filter candidate boxes
        scores = torch.tensor(scores, dtype=torch.float32)
        if torch.cuda.is_available():
            bounding_boxes_xyxy.to('cuda')
            scores.to('cuda')
        nms_start = time.perf_counter()
        keep_indices = nms(bounding_boxes_xyxy, scores, 0.4)
        nms_end = time.perf_counter()
        print(f"NMS took {nms_end - nms_start} seconds")
        class_ids = class_ids[keep_indices]
        confidences = scores[keep_indices]
        bounding_boxes = bounding_boxes_xyxy[keep_indices]
        if type(class_ids) is not np.ndarray:
            print(class_ids, type(class_ids))
            class_ids = np.array([int(class_ids)])

        for box in bounding_boxes:
            box[0] *= self.x_factor
            box[1] *= self.y_factor
            box[2] *= self.x_factor
            box[3] *= self.y_factor
        return bounding_boxes, confidences, class_ids

    def detect(self, image, visualize=True):
        input_image = image.copy()
        input_image = self.preprocess(input_image)
        outputs = self.inference(input_image)
        bounding_boxes, confidences, class_ids = self.postprocess(outputs, self.score_threshold, self.nms_threshold)
        if visualize:
            for i in range(class_ids.shape[0]):
                class_id = class_ids[i]
                confidence = confidences[i]
                box = bounding_boxes[i]
                color = self.colors[int(class_id) % len(self.colors)]
                label = self.coco_class_names[int(class_id)]

                xmin, ymin, xmax, ymax = int(box[0]), int(box[1]), int(box[2]), int(box[3])
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 2)
                cv2.rectangle(image, (xmin, ymin - 20), (xmin + 100, ymin), color, -1)
                cv2.putText(image, str(label), (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        return image


def video_detector(video_src):
    cap = cv2.VideoCapture(video_src)

    while cap.isOpened():
        success, frame = cap.read()

        if not success:
            break

        frame = yolov5.detect(frame)
        cv2.imshow("frame", frame)

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()


def image_detector(image_src):
    image = cv2.imread(image_src)
    image = yolov5.detect(image)
    cv2.imshow("image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == '__main__':
    model_path = "weights/yolov5s.onnx"
    yolov5 = YoloV5ORTInference(model_path)
    video_source = 'rtsp://admin:aoto12345@192.168.8.204:554/h264/ch1/main/av_stream'
    # video_source = 0
    video_detector(video_source)
    # image_detector("data/images/bus.jpg")
    exit(0)

```