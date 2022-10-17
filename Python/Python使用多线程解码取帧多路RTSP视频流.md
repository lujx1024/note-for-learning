---
title: Python使用多线程解码取帧多路RTSP视频流
tags: Python,多路视频取帧,多线程
renderNumberedHeading: true
grammar_cjkRuby: true
---

## 工具代码
```
# coding:utf-8
import math
import cv2
import time
import numpy as np
from threading import Thread, Lock
import re


def letterbox(im, new_shape=(640, 640), color=(114, 114, 114), auto=True, scaleFill=False, scaleup=True, stride=32):
    # Resize and pad image while meeting stride-multiple constraints
    shape = im.shape[:2]  # current shape [height, width]
    if isinstance(new_shape, int):
        new_shape = (new_shape, new_shape)

    # Scale ratio (new / old)
    r = min(new_shape[0] / shape[0], new_shape[1] / shape[1])
    if not scaleup:  # only scale down, do not scale up (for better val mAP)
        r = min(r, 1.0)

    # Compute padding
    ratio = r, r  # width, height ratios
    new_unpad = int(round(shape[1] * r)), int(round(shape[0] * r))
    dw, dh = new_shape[1] - new_unpad[0], new_shape[0] - new_unpad[1]  # wh padding
    if auto:  # minimum rectangle
        dw, dh = np.mod(dw, stride), np.mod(dh, stride)  # wh padding
    elif scaleFill:  # stretch
        dw, dh = 0.0, 0.0
        new_unpad = (new_shape[1], new_shape[0])
        ratio = new_shape[1] / shape[1], new_shape[0] / shape[0]  # width, height ratios

    dw /= 2  # divide padding into 2 sides
    dh /= 2

    if shape[::-1] != new_unpad:  # resize
        im = cv2.resize(im, new_unpad, interpolation=cv2.INTER_LINEAR)
    top, bottom = int(round(dh - 0.1)), int(round(dh + 0.1))
    left, right = int(round(dw - 0.1)), int(round(dw + 0.1))
    im = cv2.copyMakeBorder(im, top, bottom, left, right,cv2.BORDER_CONSTANT, value=color)  # add border
    return im, ratio, (dw, dh)


def clean_str(s):
    # Cleans a string by replacing special characters with underscore _
    return re.sub(pattern="[|@#!¡·$€%&()=?¿^*;:,¨´><+]", repl="_", string=s)


class LoadStreams:
    def __init__(self, sources, img_size=640, stride=32, auto=True, interval=1):
        self.mode = 'stream'
        self.img_size = img_size
        self.stride = stride
        self.interval = interval
        n = len(sources)
        self.imgs, self.fps, self.frames, self.threads = [None] * n, [0] * n, [0] * n, [None] * n
        # clean source names for later
        self.sources = [clean_str(x) for x in sources]
        self.auto = auto
        # self.queue_list = [queue.Queue(maxsize=4)] * n
        for i, s in enumerate(sources):  # index, source
            # Start thread to read frames from video stream
            st = f'{i + 1}/{n}: {s}... '
            if s.isdigit():
                s = int(s)
            cap = cv2.VideoCapture(s)
            assert cap.isOpened(), f'{st}Failed to open {s}'
            w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)  # warning: may return 0 or nan
            self.frames[i] = max(int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), 0) or float('inf')  # infinite stream fallback
            self.fps[i] = max((fps if math.isfinite(fps) else 0) % 100, 0) or 30  # 30 FPS fallback

            _, self.imgs[i] = cap.read()  # guarantee first frame
            self.threads[i] = Thread(target=self.update, args=([i, cap, s]), daemon=True)
            print(f"{st} Success ({self.frames[i]} frames {w}x{h} at {self.fps[i]:.2f} FPS)")
            self.threads[i].start()
        print('')  # newline

        # check for common shapes
        s = np.stack([letterbox(x, self.img_size, stride=self.stride, auto=self.auto)[0].shape for x in self.imgs])
        # rect inference if all shapes equal
        self.rect = np.unique(s, axis=0).shape[0] == 1
        if not self.rect:
            print('WARNING: Stream shapes differ. For optimal performance supply similarly-shaped streams.')

    def update(self, i, cap, stream):
        # Read stream `i` frames in daemon thread
        # frame number, frame array, inference every 'read' frame
        n, f, read = 0, self.frames[i], self.interval
        print('f==', f)
        while cap.isOpened() and n < f:
            n += 1
            cap.grab()
            if n % read == 0:
                if n > 1000:
                    n = read + 1
                success, im = cap.retrieve()
                if success:
                    self.imgs[i] = im
                else:
                    print(i)
                    print('WARNING: Video stream unresponsive, please check your IP camera connection.')
                    self.imgs[i] = np.zeros_like(self.imgs[i])
                    cap.open(stream)  # re-open stream if signal was lost
            time.sleep(0.001)  # wait time

    def __iter__(self):
        self.count = -1
        return self

    def __next__(self):
        self.count += 1
        if not all(x.is_alive() for x in self.threads) or cv2.waitKey(1) == ord('q'):  # q to quit
            cv2.destroyAllWindows()
            raise StopIteration

        return self.imgs

    def __len__(self):
        # 1E12 frames = 32 streams at 30 FPS for 30 years
        return len(self.sources)


if __name__ == '__main__':
    pass

```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。

## 使用代码
```

# RTSP视频流链接列表,格式如下:
# [
# "rtsp://admin:ccb12345@192.168.1.64/Streaming/Channels/101",
# "rtsp://admin:ccb12345@192.168.1.201/Streaming/Channels/101"
# ]
sources = stream_urls
source_count = len(sources)
LS = LoadStreams(sources, interval=3)

for imgs in LS:
	for i, frame in enumerate(imgs):
		if frame is None:
			print("**Frame Is None**")
			continue
		frame_height, frame_width, _ = frame.shape
```