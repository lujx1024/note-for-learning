# `ffmpeg`安装

## 1. `ubuntu`系统安装`ffmpeg`

```shell
sudo apt-get update
sudo apt-get install ffmpeg
```

查看`ffmpeg`版本
```shell
ffmpeg -version
```

# ffmpeg抽帧高清图片

指令示例:
```shell
ffmpeg -i D01_20240131142900.mp4  -r 2 -s 2560x1440 -f image2 ../frames_extract/images_D01/D01_20240131142900_%10d.png -y
```

- `-i` 输入文件
- `-r` 指定帧率，即每秒钟抽取多少帧
- `-s` 指定图片分辨率,2k分辨率为2560x1440，4k分辨率为3840x2160
- `-f` 指定图片格式