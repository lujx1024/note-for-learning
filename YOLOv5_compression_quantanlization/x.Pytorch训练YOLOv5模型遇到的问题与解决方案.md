[TOC]

# 概述

本文档主要记录在使用`Pytorch`框架训练`YOLO`系列模型过程中遇到的异常问题与报错，以及当时的环境配置和解决方案等。

# 问题记录

## 1.`OSError: [WinError 1455]` 页面文件太小，无法完成操作

**前置环境:**

- `Windows 10`操作系统
- `GeForce GTX 1660 Super`
- `CUDA v11.2` `cuDNN v8.2.1`
- `Pytorch v1.12` `YOLOv5`

**训练指令**

```bash
python train.py --data coco128.yaml --epochs 300 --weights '' --cfg yolov5s.yaml  --batch-size 64
```

**问题原因**

报的错误是`页面文件太小,无法完成操作`，所以需要调大页面文件的大小,也就是调整虚拟内存的大小。

**解决方法**

由于系统在默认情况下没有给C盘以外的磁盘分配虚拟内存，所以在程序启动时，如果虚拟环境安装在其他盘，如D盘，由于没有分配虚拟内存，自然就遇到了上面的问题。所以，要解决这个问题，手动调整虚拟环境所在盘的页面大小即可，操作步骤如下:

- 在桌面上右键单击 `此电脑`或 `我的电脑`图标，选择`属性`

- 在系统窗口中，进入`高级系统设置`
- 在系统属性窗口中，转到`高级`选项卡，并在`性能`部分点击`设置`按钮。
- 在性能选项窗口中，导航到 `高级` 选项卡，并在 `虚拟内存` 部分点击`更改`按钮。
- 取消选中 `自动管理所有驱动器的页面文件大小` 选项
- 选择出现错误的驱动器（如驱动器 `D:`），并选择`自定义大小`选项。
- 将`初始大小`和`最大大小`的值设置为较大的值（例如，初始大小和最大大小均为 10240 MB,根据实际情况动态调整）。
- 点击`设置`按钮，然后点击`确定`保存更改。
- **重新启动计算机**以使更改生效

> 注：若虚拟环境安装在C盘，部分操作可以跳过，如 ~取消选中 `自动管理所有驱动器的页面文件大小`选项~,根据实际情况调整

**参考链接**

- [CSDN](https://blog.csdn.net/weixin_46133643/article/details/125042903)【`WinError 1455]页面文件太小，无法完成操作 解决方案`】
- [阿里云](https://developer.aliyun.com/article/1142444)【解决方案】`OSError: [WinError 1455]`页面文件太小，无法完成操作



## 2.启动训练报错`RuntimeError: Unable to find a valid cuDNN algorithm to run convolution`

**前置环境:**

- `Windows 10`操作系统
- `GeForce GTX 1660 Super`
- `CUDA v11.2` `cuDNN v8.2.1`
- `Pytorch v1.12` `YOLOv5`

**训练指令**

```bash
python train.py --data coco128.yaml --epochs 300 --weights '' --cfg yolov5s.yaml  --batch-size 64
```

**问题原因**

报错的原因是显卡**显存太小**，训练无法启动，需要将`batch-size`调小即可

**参考链接**

- [CSDN](https://blog.csdn.net/wxd1233/article/details/120509750)
- [`Stackoverflow`](https://stackoverflow.com/questions/61467751/unable-to-find-a-valid-cudnn-algorithm-to-run-convolution)

## 3. yolo系列算法训练时loss出现nan值，解决办法（GTX16xx系列显卡的问题）

**前置环境:**

- `Windows 10`操作系统
- `GeForce GTX 1660 Super`
- `CUDA v11.2` `cuDNN v8.2.1`
- `Pytorch v1.12` `YOLOv5`

**训练指令**

```bash
python train.py --data coco128.yaml --epochs 300 --weights '' --cfg yolov5s.yaml  --batch-size 8
```

**问题原因**

`NVIDIA GeForce GTX 16`系列显卡使用高版本`CUDA`时，会导致`Pytorch`在半精度(`fp16`)运算是出现`NAN`

> 注: 由于检索到的资料有限，不确定是否除 `GTX 16系显卡和CUDA v11.x`之外的组合会有同样的问题



**解决方法**

修改训练文件`train.py`，将`amp`置为`False`. 注释掉源代码中`train`方法中的`amp = check_amp(model)`,可全局搜索，代码如下 :

```python
# amp = check_amp(model)  # check AMP  注释掉这一行
amp=False 添加这一行
```

修改完成后继续执行训练任务即可。

> 注: 有部分资料显示通过降低`Pytorch`和`CUDA`版本的方法同样可以规避此问题，如`Pytorch v1.10` 和 `CUDA v10.2`但是由于版本过于老旧或官方不再支持等原因，不推荐使用

**参考链接**

- [CSDN](https://blog.csdn.net/weixin_55249340/article/details/125855686)
- [知乎](https://zhuanlan.zhihu.com/p/443166496)
- [CSDN](https://blog.csdn.net/qq_51208442/article/details/126636768)



## 4.运行`detect.py`报错`AttributeError: 'Upsample' object has no attribute 'recompute_scale_factor'`

**前置环境:**

- `Windows 10`操作系统
- `GeForce GTX 1660 Super`
- `CUDA v11.2` `cuDNN v8.2.1`
- `Pytorch v1.12` `YOLOv5`

**操作指令**

```bash
python .\detect.py --source .\data\images\ --weights .\weights\yolov5l.pt --conf 0.4
```

**问题原因**

是由于 `PyTorch`版本问题。从`PyTorch 1.6.0`开始，`nn.Upsample` 已经不再支持 `recompute_scale_factor` 参数。所以，如果使用的是`PyTorch 1.6.0`或更高版本，尝试使用一个保存的模型（它是在旧版本的 `PyTorch` 中创建的，当时 `recompute_scale_factor` 参数是可用的）,就可能会遇到这个问题.

**报错信息**

```bash
# 执行指令
(yolo_slim)E:\..\..\yolov5-6.1-slimming > python .\detect.py --source .\data\images\ --weights .\weights\yolov5l.pt --conf 0.4

detect: weights=['.\\weights\\yolov5l.pt'], source=.\data\images\, data=data\coco128.yaml, imgsz=[640, 640], conf_thres=0.4, iou_thres=0.45, max_det=1000, device=, view_img=False, save_txt=False, save_conf=False, save_crop=False, nosave=False, classes=None, agnostic_nms=False, augment=False, visualize=False, update=False, project=runs\detect, name=exp, exist_ok=False, line_thickness=3, hide_labels=False, hide_conf=False, half=False, dnn=False
YOLOv5  2022-2-22 torch 1.12.1 CUDA:0 (NVIDIA GeForce GTX 1660 SUPER, 6144MiB)

Traceback (most recent call last):
  File ".\detect.py", line 257, in <module>
    main(opt)
  File ".\detect.py", line 252, in main
    run(**vars(opt))
  File "D:\conda_envs\envs\yolo_slim\lib\site-packages\torch\autograd\grad_mode.py", line 27, in decorate_context
    return func(*args, **kwargs)
  File ".\detect.py", line 113, in run
    model.warmup(imgsz=(1 if pt else bs, 3, *imgsz), half=half)  # warmup
  File "E:\python\python_project\yolov5-6.1-slimming\models\common.py", line 463, in warmup
    self.forward(im)  # warmup
  File "E:\python\python_project\yolov5-6.1-slimming\models\common.py", line 402, in forward
    y = self.model(im) if self.jit else self.model(im, augment=augment, visualize=visualize)
  File "D:\conda_envs\envs\yolo_slim\lib\site-packages\torch\nn\modules\module.py", line 1130, in _call_impl
    return forward_call(*input, **kwargs)
  File "E:\python\python_project\yolov5-6.1-slimming\models\yolo.py", line 127, in forward
    return self._forward_once(x, profile, visualize)  # single-scale inference, train
  File "E:\python\python_project\yolov5-6.1-slimming\models\yolo.py", line 150, in _forward_once
    x = m(x)  # run
  File "D:\conda_envs\envs\yolo_slim\lib\site-packages\torch\nn\modules\module.py", line 1130, in _call_impl
    return forward_call(*input, **kwargs)
  File "D:\conda_envs\envs\yolo_slim\lib\site-packages\torch\nn\modules\upsampling.py", line 154, in forward
    recompute_scale_factor=self.recompute_scale_factor)
  File "D:\conda_envs\envs\yolo_slim\lib\site-packages\torch\nn\modules\module.py", line 1207, in __getattr__
    raise AttributeError("'{}' object has no attribute '{}'".format(
AttributeError: 'Upsample' object has no attribute 'recompute_scale_factor'
```

**解决方法**

1. **(不建议)**降低`Pytorch`版本，将版本降低到`1.10`或以下。由于`Pytorch`与`CUDA`等环境版本有强匹配关系，贸然降低版本可能会引发其他问题，非特殊情况不建议使用

2. 修改`Pytorch`源码

   根据错误提示，定位到虚拟环境中的源代码位置: `<virtual_env_dir>/lib/site-packages/torch/nn/modules/upsampling.py`, `Upsample`类`forward`方法，约153行代码，注释掉`recompute_scale_factor=self.recompute_scale_factor`参数即可，如下所示:

   

   **改动前：**

   ```python
       def forward(self, input: Tensor) -> Tensor:
           return F.interpolate(input, self.size, self.scale_factor, self.mode, self.align_corners,
                                recompute_scale_factor=self.recompute_scale_factor)
   ```

   **改动后：**

   ```python
       def forward(self, input: Tensor) -> Tensor:
           return F.interpolate(input, self.size, self.scale_factor, self.mode, self.align_corners）
                             #   recompute_scale_factor=self.recompute_scale_factor)
   ```

   再次运行后，程序运行正常

**参考链接**

- [CSDN](https://blog.csdn.net/Thebest_jack/article/details/124723687?ydreferer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8%3D)
- [GitHub](https://github.com/ultralytics/yolov5/issues/6948)



## 5.运行`train.py`报错`AttributeError: module 'numpy' has no attribute 'int'.`

**前置环境:**

- `Windows 10`操作系统
- `GeForce GTX 1660 Super`
- `CUDA v11.2` `cuDNN v8.2.1`
- `Pytorch v1.12` `YOLOv5`

**操作指令**

```bash
python .\train.py --data .\data\voc_ball.yaml --cfg .\models\yolov5s_ball.yaml --weights .\weights\yolov5s.pt --batch-size 4 --epoch 100 --workers 4 --name yolov5s-baseline
```

**问题原因**

环境中安装的`NumPy`版本过高，`np.int`在`numpy 1.20`版本被标记为过时方法，在`NumPy 1.24`版本中被移除.

**报错信息**

```bash
Traceback (most recent call last):
  File ".\train.py", line 643, in <module>
    main(opt)
  File ".\train.py", line 539, in main
    train(opt.hyp, opt, device, callbacks)
  File ".\train.py", line 223, in train
    train_loader, dataset = create_dataloader(train_path, imgsz, batch_size // WORLD_SIZE, gs, single_cls,
  File "E:\python\python_project\yolov5-6.1-slimming\utils\datasets.py", line 100, in create_dataloader
    dataset = LoadImagesAndLabels(path, imgsz, batch_size,
  File "E:\python\python_project\yolov5-6.1-slimming\utils\datasets.py", line 443, in __init__
    bi = np.floor(np.arange(n) / batch_size).astype(np.int)  # batch index
  File "D:\conda_envs\envs\yolo_slim\lib\site-packages\numpy\__init__.py", line 305, in __getattr__
    raise AttributeError(__former_attrs__[attr])
AttributeError: module 'numpy' has no attribute 'int'.
`np.int` was a deprecated alias for the builtin `int`. To avoid this error in existing code, use `int` by itself. Doing this will not modify any behavior and is safe. When replacing `np.int`, you may wish to use e.g. `np.int64` or `np.int32` to specify the precision. If you wish to review your current use, check the release note link for additional information.
The aliases was originally deprecated in NumPy 1.20; for more details and guidance see the original release note at:
    https://numpy.org/devdocs/release/1.20.0-notes.html#deprecations
```

**解决方法**

1. 降低`NumPy`版本，为适配其他依赖库的使用，尽量降低版本到`NumPy 1.24`一下
2. 修改源代码中`np.int`为`np.int_`，或直接修改为`int`



## 6.训练时报错`TypeError: No loop matching the specified signature and casting was found for ufunc greater`

**前置环境:**

- `Windows 10`操作系统
- `GeForce GTX 1660 Super`
- `CUDA v11.2` `cuDNN v8.2.1`
- `Pytorch v1.12` `YOLOv5`

**操作指令**

```bash
python .\train.py --data .\data\voc_ball.yaml --cfg .\models\yolov5s_ball.yaml --weights .\weights\yolov5s.pt --batch-size 4 --epoch 100 --workers 4 --name yolov5s-baseline
```

**问题原因**

环境中安装的`NumPy`版本过高，`np.int`在`numpy 1.20`版本被标记为过时方法，在`NumPy 1.24`版本中被移除.

**报错信息**

```bash
Traceback (most recent call last):
  File "train_sparsity.py", line 682, in <module>
    main(opt)
  File "train_sparsity.py", line 578, in main
    train(opt.hyp, opt, device, callbacks)
  File "train_sparsity.py", line 423, in train
    callbacks.run('on_fit_epoch_end_prune', bn_weights.numpy(), epoch)
  File "E:\python\python_project\yolov5-6.1-slimming\utils\callbacks.py", line 79, in run
    logger['callback'](*args, **kwargs)
  File "E:\python\python_project\yolov5-6.1-slimming\utils\loggers\__init__.py", line 138, in on_fit_epoch_end_prune
    self.tb.add_histogram('bn_weights/hist', bn_weights, epoch, bins='doane')
  File "D:\conda_envs\envs\yolo_slim\lib\site-packages\torch\utils\tensorboard\writer.py", line 484, in add_histogram
    histogram(tag, values, bins, max_bins=max_bins), global_step, walltime
  File "D:\conda_envs\envs\yolo_slim\lib\site-packages\torch\utils\tensorboard\summary.py", line 352, in histogram
    hist = make_histogram(values.astype(float), bins, max_bins)
  File "D:\conda_envs\envs\yolo_slim\lib\site-packages\torch\utils\tensorboard\summary.py", line 380, in make_histogram
    cum_counts = np.cumsum(np.greater(counts, 0, dtype=np.int32))
TypeError: No loop matching the specified signature and casting was found for ufunc greater



## 修改 
cum_counts = np.cumsum(np.greater(counts, 0, dtype=np.int32))
cum_counts = np.cumsum(np.greater(counts, 0, dtype=float))

```

**解决方法**

修改文件`"D:\conda_envs\envs\yolo_slim\lib\site-packages\torch\utils\tensorboard\summary.py"`, 约380行, 函数`make_histogram`中的代码，如下所示:

```python
# 修改前:
cum_counts = np.cumsum(np.greater(counts, 0, dtype=np.int32))
# 修改后:
cum_counts = np.cumsum(np.greater(counts, 0))
```

## 7. yolov5训练时报错`attributeerror: ‘FreeTypeFont‘ object has no attribute ‘getsize‘`


报错原因是`Pillow`版本过高，`Pillow 10+`版本中`ImageFont`模块中的`getsize`方法被移除，因此需要降低`Pillow`版本

**解决方法**

```bash
pip install Pillow==9.5 --force-reinstall
```
##  8.YOLOv5模型导出为engine时报错`onnx-＞trt F16:Subnormal FP16 value detected`


官方回复此警告可忽略
参考链接：[官方论坛](https://forums.developer.nvidia.com/t/subnormal-fp16-values-detected/220070)
[CSDN](https://blog.csdn.net/Zhou_yongzhe/article/details/127289947)
