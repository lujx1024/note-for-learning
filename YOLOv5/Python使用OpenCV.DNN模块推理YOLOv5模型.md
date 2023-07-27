[TOC]

# 概述

本文档主要描述`python`平台，使用`opencv-python`深度神经网络模块`dnn`,推理`YOLOv5`模型的方法。

文档主要包含以下内容：

- `opencv-python`模块的安装
- `YOLOv5`模型格式的说明
- `ONNX`格式模型的加载
- 图片数据的预处理
- 模型推理
- 推理结果后处理，包括`NMS`,`cxcywh`坐标转换为`xyxy`坐标等
- 关键方法的调用与参数说明
- 完整的示例代码


# 1. 环境部署

## `YOLOv5`算法`ONNX`模型获取

可通过官方链接下载YOLOv5的官方预训练模型，模型格式为`pt`.[下载链接](https://github.com/ultralytics/yolov5/releases/download/v6.1/yolov5s.pt)
`YOLOv5`官方项目提供了`pt`格式模型转换为`ONNX`格式模型的脚本，[项目链接](https://github.com/ultralytics/yolov5)

模型导出指令：

```bash
python export --weights yolov5s.pt --include onnx
```
> 注：导出文件执行指令所需环境安装配置参考官方项目`README`文档即可，不在赘述。

## `opencv-python`模块安装

1. 创建虚拟环境并激活

   ```bash
   conda create -n opencv python=3.8 -y
   conda activate opencv
   ```

2. `pip`安装`opencv-python`模块

   ```bash
   pip install opencv-python
   ```
    > 注: 通过`pip`安装`opencv-python`模块时，默认安装仅支持`CPU`推理，如需支持`GPU`推理，需从源码编译安装，具体安装方法较复杂，这里不在赘述。


# 2.关键代码

## 2.1 模型加载

`opencv-python`模块提供了`readNetFromONNX`方法，用于加载`ONNX`格式模型。


```python
import cv2
cv2.dnn.readNetFromONNX(model_path)
```

## 2.2 图片数据预处理

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

## 2.3 模型推理

1. 设置推理Backend和Target

   

   ```python
   model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
   model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
   ```
    模型加载完成后，需要设置推理时的设备，一般情况下，推理设备为`CPU`，设置方法如下：

    ```python
    model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    ```

    当然，若此时环境中的`opencv-python`模块支持`GPU`推理，也可以设置为`GPU`推理，设置方法如下：

    ```python
    model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
    model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    ```

    > 注: 判断`opencv-python`模块是否支持`GPU`推理的方法如下：`cv2.cuda.getCudaEnabledDeviceCount()`,返回值大于0表示支持`GPU`推理，否则表示不支持。

2. 设置模型输入数据

   ```python
   model.setInput(blob)
   ```

   `blob`为上一步数据预处理得到的数据。

3. 调用模型前向传播`forward`方法
   ```
   outputs = model.forward()
   ```

    `outputs`为模型推理的输出，输出格式为(1,25200,5+nc),`25200`为模型输出的网格数量，`5+nc`为每个网格预测的`5+nc`个值，`5`为`x,y,w,h,conf`，`nc`为类别数量。

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

# 3. 示例代码(可运行)

源代码一共有两份，其中一份是函数的拼接与调用，比较方便调试，另一份是封装成类，方便集成到其他项目中。

## 3.1 未封装

```python
"""
running the onnx model inference with opencv dnn module

"""
from typing import List

import cv2
import numpy as np
import time
from pathlib import Path


def build_model(model_path: str) -> cv2.dnn_Net:
    """
    build the model with opencv dnn module
    Args:
        model_path: the path of the model, the model should be in onnx format

    Returns:
        the model object
    """
    # check if the model file exists
    if not Path(model_path).exists():
        raise FileNotFoundError(f"model file {model_path} not found")
    model = cv2.dnn.readNetFromONNX(model_path)

    # check if the opencv-python in your environment supports cuda
    cuda_available = cv2.cuda.getCudaEnabledDeviceCount() > 0

    if cuda_available:  # if cuda is available, use cuda
        model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    else:  # if cuda is not available, use cpu
        model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
    return model


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

    # the alternative way to get the blob
    # rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # input_image = cv2.resize(src=rgb, dsize=(INPUT_WIDTH, INPUT_HEIGHT))
    # blob_img = np.float32(input_image) / 255.0
    # input_x = blob_img.transpose((2, 0, 1))
    # blob = np.expand_dims(input_x, 0)

    if cv2.cuda.getCudaEnabledDeviceCount() > 0:
        model.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
        model.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
    else:
        model.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        model.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)

    # set the input data
    model.setInput(blob)

    start = time.perf_counter()
    # inference
    outs = model.forward()

    end = time.perf_counter()

    print("inference time: ", end - start)

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

    indices = cv2.dnn.NMSBoxes(output_data[:, 0:4].tolist(), output_data[:, 4].tolist(), 0.6, 0.4)

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
        #
        # find the least and most probable classes' indices and their probabilities
        # min_val, max_val, min_loc, mac_loc = cv2.minMaxLoc(class_prediction_probability)
        most_probable_class_index = np.argmax(class_prediction_probability)
        label = labels[most_probable_class_index]
        confidence = float(confidence)

        # bounding_boxes.append(box)
        # confidences.append(confidence)
        # class_ids.append(most_probable_class_index)

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

        # 4. wrap the detection result
        class_ids, confidences, boxes = wrap_detection(input_image, output_data[0], coco_class_names)

        # 5. draw the detection result on the frame
        for (class_id, confidence, box) in zip(class_ids, confidences, boxes):
            color = colors[int(class_id) % len(colors)]
            label = coco_class_names[int(class_id)]

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
    model_path = Path("weights/yolov5s.onnx")
    net = build_model(str(model_path))
    # 2. load the video capture
    # video_source = 0
    video_source = 'rtsp://admin:aoto12345@192.168.8.204:554/h264/ch1/main/av_stream'
    video_detector(video_source)

    exit(0)
```

## 3.2 封装成类调用

```python
from typing import List

import onnx
from torchvision import transforms

from torchvision.ops import nms,box_convert
import cv2
import time
import numpy as np
import onnxruntime as ort
import torch

INPUT_WIDTH = 640
INPUT_HEIGHT = 640

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

    nms_start = time.perf_counter()
    indices = cv2.dnn.NMSBoxes(output_data[:, 0:4].tolist(), output_data[:, 4].tolist(), 0.6, 0.4)
    nms_finish = time.perf_counter()
    print(f"nms time: {nms_finish - nms_start}")
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
        #
        # find the least and most probable classes' indices and their probabilities
        # min_val, max_val, min_loc, mac_loc = cv2.minMaxLoc(class_prediction_probability)
        most_probable_class_index = np.argmax(class_prediction_probability)
        label = labels[most_probable_class_index]
        confidence = float(confidence)

        # bounding_boxes.append(box)
        # confidences.append(confidence)
        # class_ids.append(most_probable_class_index)

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

colors = np.random.uniform(0, 255, size=(len(coco_class_names), 3))
if __name__ == '__main__':
    # Load the model
    model_path = "weights/yolov5s.onnx"
    onnx_model = onnx.load(model_path)
    onnx.checker.check_model(onnx_model)
    session = ort.InferenceSession(model_path, providers=['CUDAExecutionProvider',"CPUExecutionProvider"])
    capture = cv2.VideoCapture(0)

    trans = transforms.Compose([
        transforms.Resize((640, 640)),
        transforms.ToTensor()
    ])

    from PIL import Image

    while capture.isOpened():
        success, frame = capture.read()
        start = time.perf_counter()
        if not success:
            break
        rows, cols, channels = frame.shape
        # Preprocessing
        max_size = max(rows, cols)
        input_image = np.zeros((max_size, max_size, 3), dtype=np.uint8)
        input_image[:rows, :cols, :] = frame
        input_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2RGB)

        inputs = trans(Image.fromarray(input_image))
        inputs = inputs.unsqueeze(0)
        print(inputs.shape)
        # inputs.to('cuda')
        ort_inputs = {session.get_inputs()[0].name: inputs.numpy()}
        ort_outs = session.run(None, ort_inputs)
        out_prob = ort_outs[0][0]
        print(out_prob.shape)

        scores = out_prob[:, 4] # Confidence scores are in the 5th column (0-indexed)
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
        bounding_boxes_xyxy.to('cuda')
        scores.to('cuda')
        nms_start = time.perf_counter()
        keep_indices = nms(bounding_boxes_xyxy, scores, 0.4)
        nms_end = time.perf_counter()
        print(f"NMS took {nms_end - nms_start} seconds")
        class_ids = class_ids[keep_indices]
        confidences = scores[keep_indices]
        bounding_boxes = bounding_boxes_xyxy[keep_indices]

        # class_ids, confidences, bounding_boxes = wrap_detection(input_image, out_prob[0], coco_class_names, 0.6)
        # break

        for i in range(len(keep_indices)):
            try:
                class_id = class_ids[i]
            except IndexError as e:
                print(e)
                print(class_ids,i, len(keep_indices))
                break
            confidence = confidences[i]
            box = bounding_boxes[i]
            color = colors[int(class_id) % len(colors)]
            label = coco_class_names[int(class_id)]

            # cv2.rectangle(frame, box, color, 2)

            print(type(box), box[0], box[1], box[2], box[3], box)
            xmin, ymin, xmax, ymax = int(box[0]), int(box[1]), int(box[2]), int(box[3])
            cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
            # cv2.rectangle(frame, box, color, 2)
            # cv2.rectangle(frame, [box[0], box[1], box[2], box[3]], color, thickness=2)

            cv2.rectangle(frame, (xmin, ymin - 20), (xmin + 100, ymin), color, -1)
            cv2.putText(frame, str(label), (xmin, ymin - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

        finish = time.perf_counter()
        FPS = round(1.0 / (finish - start), 2)
        cv2.putText(frame, f"FPS: {str(FPS)}", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
        # 6. show the frame
        cv2.imshow("frame", frame)

        # 7. press 'q' to exit
        if cv2.waitKey(1) == ord('q'):
            break

    # 8. release the capture and destroy all windows
    capture.release()
    cv2.destroyAllWindows()

    exit(0)
```
