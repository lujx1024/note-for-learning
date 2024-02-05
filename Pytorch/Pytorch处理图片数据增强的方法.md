[TOC]

# 概述

本文主要介绍如何使用`Pytorch`提供的`transforms`模块实现图像分类。

# 关键模块

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

