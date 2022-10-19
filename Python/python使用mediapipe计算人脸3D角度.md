---
title: python使用mediapipe计算人脸3D角度
tags: Python,mediapipe,人脸角度
renderNumberedHeading: true
grammar_cjkRuby: true
---
## 安装依赖
```bash
pip install numpy opencv-python mediapipe
```

## 代码示例
```python?linenums
from typing import Tuple

import numpy as np
import cv2
from mediapipe.python.solutions.face_mesh import FaceMesh


def get_face_angles(image: np.ndarray, face_mesh: FaceMesh) -> Tuple:
    """
    使用mediapipe工具计算人脸的俯仰角、偏航角以及旋转角
    Args:
        image: numpy.ndarray数据格式的图片数据
        face_mesh: mediapipe人脸处理工具

    Returns: (x, y, z) x为俯仰角，y为偏航角，z为旋转角

    """
    try:
        # 处理图片，先左右翻转，再改变颜色通道为RGB
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    except Exception as e:
        print(e)
        # 图片数据异常，则返回None
        return None, None, None
    image.flags.writeable = False

    # 获取人脸关键点检测数据
    results = face_mesh.process(image)  # NamedTuple
    image.flags.writeable = True
    # 图片颜色通道改为BGR分布
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    # 获取原始图片的宽与高
    img_h, img_w, img_c = image.shape
    face_3d = []
    face_2d = []

    # 没有识别到人脸关键点(可能原因为图片质量过低)，返回角度为None
    if results.multi_face_landmarks is None or len(results.multi_face_landmarks) <= 0:
        return [None] * 3

    # 默认只处理单张人脸图片
    # TODO 多人脸图片此处需要循环处理
    face_landmarks = results.multi_face_landmarks[0]

    nose_landmark = face_landmarks.landmark[1]
    nose_2d = (nose_landmark.x * img_w, nose_landmark.y * img_h)
    nose_3d = (nose_landmark.x * img_w, nose_landmark.y * img_h, nose_landmark.z * 3000)
    for index in [1, 33, 61, 199, 263, 291]:
        lm = face_landmarks.landmark[index]
        x, y = int(lm.x * img_w), int(lm.y * img_h)
        face_2d.append([x, y])
        face_3d.append([x, y, lm.z])

    face_2d = np.array(face_2d, dtype=np.float64)
    face_3d = np.array(face_3d, dtype=np.float64)

    facial_length = 1 * img_w
    cam_matrix = np.array([[facial_length, 0, img_h / 2], [0, facial_length, img_w / 2], [0, 0, 1]])
    dist_matrix = np.zeros((4, 1), dtype=np.float64)
    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
    rmat, jac = cv2.Rodrigues(rot_vec)

    # 此时angles的成员均为归一化后的(0,1)之间的数据，
    angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

    # 将数值值*360转换为正常的角度值
    x, y, z = tuple(map(lambda i: i * 360, angles))

    return x, y, z
```

## 调用方式

```python
# 默认test.jpg图片中只有一张人脸图片
image = cv2.imread('images/test.jpg')  
x, y, z= get_face_angles(image, face_mesh)
```
欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。