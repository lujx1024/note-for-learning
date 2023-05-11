---
title: Python调用FFmpeg批量抽帧视频
tags: Python,FFmpeg,视频抽帧
renderNumberedHeading: true
grammar_cjkRuby: true
---


```
import subprocess
from os import makedirs
from os.path import abspath,join,basename


import os
from tqdm import tqdm
import shutil

def list_files(startpath):
    """
    获取当前路径下的所有子文件,包含子文件夹下的所有文件

    Args:
        startpath (str): 文件路径,可以是目录或文件路径

    Yields:
        List: 当前文件夹下的所有子文件列表
    """
    stack = [startpath]
    while stack:
        folder = stack.pop()
        for file in os.listdir(folder):
            path = os.path.join(folder, file)
            if os.path.isdir(path):
                stack.append(path)
            else:
                yield path


# step 1. 确认视频源目录和图片目标目录
tmp_video_dir = fr"C:\Users\lujx\Desktop\test"
target_pic_dir = fr"C:\Users\lujx\Desktop\test\imgs"
makedirs(target_pic_dir,exist_ok=True)

# step 2. 获取所有的视频文件地址
video_formats = ('.mp4',".mkv",".avi")
video_filelist = [os.path.abspath(os.path.join(tmp_video_dir,item)) for item in os.listdir(tmp_video_dir) if item.endswith(video_formats)]


# strp 3. 循环处理视频抽帧
for filename in tqdm(video_filelist):
    
    # 每个视频的抽帧图片分别保存到不同的文件夹
    output_dir = abspath(join(target_pic_dir,basename(filename)))
    makedirs(output_dir,exist_ok= True)

    # 指定本地的ffmpeg安装位置，拼接抽帧指令
    path_to_ffmpeg = fr"D:\media-autobuild_suite-master\local64\bin-video\ffmpeg.exe"
    ffmpeg_cmd = [path_to_ffmpeg,'-err_detect', 'ignore_err', "-i", filename,'-q:v' ,'1', "-vf" ,'fps=3, scale=1920:1080', "-f", "image2", fr"{output_dir}\image_%08d.jpg"]

    # 执行指令
    subprocess.run(ffmpeg_cmd)

```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。