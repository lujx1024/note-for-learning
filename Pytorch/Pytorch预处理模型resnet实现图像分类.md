[TOC]

# 概述

本文主要介绍如何使用Pytorch提供的`resnet`预处理模型实现图像分类。

# 关键模块

## 预训练模型实例

`torchvision`提供了一些预训练模型，可以直接使用，如下所示：

```python
from torchvision import models

model = models.resnet101(pretrained=True)
```

## 图像预处理

`torchvision`提供了一些图像预处理方法，如下所示：

```python
from torchvision import transforms

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])
```

> `resnet``模型的输入图像大小为`224x224`，因此需要对图像大小进行预处理。


## 图像分类推理

```python
from PIL import Image
import torch

img = Image.open('img.jpg')
img_t = transform(img)
batch_t = torch.unsqueeze(img_t, 0)

model.eval()
with  torch.no_grad():
    out = model(batch_t)
```

## 推理结果后处理

```python
from  torch.nn import functional as F

probabilities = F.softmax(out, dim=1)[0] * 100

prob,classes = probabilities.topk(5)
```

## 结果展示

```python
import pandas as pd
categories = pd.read_csv("https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt",header=None)

for i in range(5):
    print(categories[0][classes[i]],prob[i].item())
```


# 完整代码

```python
from torchvision import models
from torchvision import transforms
from PIL import Image
import torch
from  torch.nn import functional as F
import pandas as pd

model = models.resnet101(pretrained=True)

transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

img = Image.open('img.jpg')

img_t = transform(img)

batch_t = torch.unsqueeze(img_t, 0)

model.eval()

with  torch.no_grad():
    out = model(batch_t)

probabilities = F.softmax(out, dim=1)[0] * 100

prob,classes = probabilities.topk(5)

categories = pd.read_csv("https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt",header=None)

for i in range(5):
    print(categories[0][classes[i]],prob[i].item())
```

