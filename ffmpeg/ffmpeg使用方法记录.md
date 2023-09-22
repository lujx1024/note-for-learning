# 安装

# 命令行使用

这里指`FFMPEG`提供的命令行（`CLI`）工具`ffmpeg`，其使用方法如下（方括号表示可选项，花括号表示必选项目）:

```bash
ffmpeg [global options] {[infile options] ['-i' 'infile'] ...} {[outfile options] 'outfile' ...}
```

参数选项由三部分组成: 

- 可选的一组全局参数
- 一组或多组输入文件参数
- 一组或多组输出文件参数，
> 注 : 每组输入文件参数以`-i`为结束标记；每组输出文件参数以`输出文件名`为结束标记。

## 基本选项

### 能力集列表

- `-formats`: 列出支持的文件格式。
- `-codecs`: 列出支持的编解码器。
- `-decoders`: 列出支持的解码器。
- `-encoders`: 列出支持的编码器。
- `-protocols`: 列出支持的协议。
- `-bsfs`: 列出支持的比特流过滤器。
- `-filters`: 列出支持的滤镜。
- `-pix_fmts`: 列出支持的图像采样格式。
- `-sample_fmts`: 列出支持的声音采样格式。

### 常用输入选项

- `-i filename`: 指定输入文件名。
- `-f fmt`: 强制设定文件格式，需使用[能力集列表](#能力集列表)中的名称（缺省是根据扩展名选择的）。
- `-ss hh:mm:ss[.xxx]`: 设定输入文件的起始时间点，启动后将跳转到此时间点然后开始读取数据。

    > 对于输入，以下选项通常是自动识别的，但也可以强制设定。

- `-c codec`: 指定解码器，需使用[能力集列表](#能力集列表)中的名称。
- `-acodec codec`: 指定声音的解码器，需使用[能力集列表](#能力集列表)中的名称。
- `-vcodec codec`: 指定视频的解码器，需使用[能力集列表](#能力集列表)中的名称。
- `-b:v bitrate`: 设定视频流的比特率，整数，单位bps。
- `-r fps`: 设定视频流的帧率，整数，单位fps。
- `-s WxH`: 设定视频的画面大小。也可以通过挂载画面缩放滤镜实现。
- `-pix_fmt format`: 设定视频流的图像格式（如RGB还是YUV）。
- `-ar sample rate`: 设定音频流的采样率，整数，单位Hz。
- `-ab bitrate`: 设定音频流的比特率，整数，单位bps。
- `-ac channels`: 设置音频流的声道数目。

### 常用输出选项

- `-f fmt`: 强制设定文件格式，需使用[能力集列表](#能力集列表)中的名称（缺省是根据扩展名选择的）。
- `-c codec`: 指定编码器，需使用[能力集列表](#能力集列表)中的名称（编码器设定为`copy`表示不进行编解码）。
- `-acodec codec`: 指定声音的编码器，需使用[能力集列表](#能力集列表)中的名称（编码器设定-为`copy`表示不进行编解码）。
- `-vcodec codec`: 指定视频的编码器，需使用[能力集列表](#能力集列表)中的名称（编解码器设定为`copy`表示不进行编解码）。
- `-r fps`: 设定视频编码器的帧率，整数，单位`fps`。
- `-pix_fmt format`: 设置视频编码器使用的图像格式（如`RGB`还是`YUV`）。
- `-ar sample rate`: 设定音频编码器的采样率，整数，单位`Hz`。
- `-b bitrate`: 设定音视频编码器输出的比特率，整数，单位`bps`。
- `-ab bitrate`: 设定音频编码器输出的比特率，整数，单位`bps`。
- `-ac channels`: 设置音频编码器的声道数目。
- `-an` 忽略任何音频流。
- `-vn` 忽略任何视频流。
- `-t hh:mm:ss[.xxx]`: 设定输出文件的时间长度。
- `-to hh:mm:ss[.xxx]`: 如果没有设定输出文件的时间长度,可以设定终止时间点。

### 流标识

FFMPEG的某些选项可以对一个特定的媒体流起作用，这种情况下需要在选项后面增加一个流标识。流标识允许以下几种格式:

- `流序号`。譬如`:1`”`表示第二个流。
- `流类型`。譬如`:a`表示音频流，流类型可以和流序号合并使用，譬如`:a:1`表示第二个音频流。
- `节目`。节目和流序号可以合并使用。
- `流标识`。流标识是一个内部标识号。
假如要设定第二个音频流为`copy`，则需要指定`-codec:a:1 copy`

### 音频选项

- `-aframes`: 等价于`frames:a`，输出选项，用于指定输出的音频帧数目。
- `-aq`: 等价于`q:a`，老版本为`qscale:a`，用于设定音频质量。
- `-atag`: 等价于`tag:a`，用于设定音频流的标签。
- `-af`: 等价于`filter:a`，用于设定一个声音的后处理过滤链，其参数为一个描述声音后处理链的字符串。

### 视频选项

- `-vframes`: 等价于`frames:v`，输出选项，用于指定输出的视频帧数目。
- `-aspect`: 设置宽高比，如`4:3`、`16:9`、`1.3333`、`1.7777`等。
- `-bits_per_raw_sample`: 设置每个像素点的比特数。
- `-vstats`: 产生video统计信息。
- `-vf`: 等价于`filter:v`，用于设定一个图像的后处理过滤链，其参数为一个描述图像后处理链的字符串。
- `-vtag`: 等价于`tag:v`，用于设定视频流的标签。
- `-force_fps`: 强制设定视频帧率。
- `-force_key_frames`: 显式控制关键帧的插入，参数为字符串，可以是一个时间戳，也可以是一个`expr:`前缀的表达式。如`-force_key_frames 0:05:00`  `-force_key_frames expr:gte(t,n_forced*5)`

### 滤镜选项
### 高级选项

- `-re`: 要求按照既定速率处理输入数据，这个速率即是输入文件的帧率。
- `-map`: 指定输出文件的流映射关系。例如 `-map 1:0 -map 1:1`要求将第二个输入文件的第一个流和第二个流写入到输出文件。如果没有`-map`选项，ffmpeg采用缺省的映射关系

## 常用指令

1. 查看硬件加速支持列表

   ```bash
   ffmpeg -hwaccels

   # 输出
   Hardware acceleration methods:
   cuda
   dxva2
   qsv
   d3d11va
   opencl
   vulkan
   ```

2. 查看NVIDIA GPU支持的编解码选项

    ```bash
    ffmpeg -codecs | grep cuvid
    
    DEV.L. av1                  Alliance for Open Media AV1 (decoders: libdav1d libaom-av1 av1 av1_cuvid av1_qsv ) (encoders: libaom-av1 librav1e libsvtav1 )
    DEV.LS h264                 H.264 / AVC / MPEG-4 AVC / MPEG-4 part 10 (decoders: h264 h264_qsv h264_cuvid ) (encoders: libx264 libx264rgb h264_amf h264_mf h264_nvenc h264_qsv )
    DEV.L. hevc                 H.265 / HEVC (High Efficiency Video Coding) (decoders: hevc hevc_qsv hevc_cuvid ) (encoders: libx265 hevc_amf hevc_mf hevc_nvenc hevc_qsv )
    DEVIL. mjpeg                Motion JPEG (decoders: mjpeg mjpeg_cuvid mjpeg_qsv ) (encoders: mjpeg mjpeg_qsv )
    DEV.L. mpeg1video           MPEG-1 video (decoders: mpeg1video mpeg1_cuvid )
    DEV.L. mpeg2video           MPEG-2 video (decoders: mpeg2video mpegvideo mpeg2_qsv mpeg2_cuvid ) (encoders: mpeg2video mpeg2_qsv )
    DEV.L. mpeg4                MPEG-4 part 2 (decoders: mpeg4 mpeg4_cuvid ) (encoders: mpeg4 libxvid )
    D.V.L. vc1                  SMPTE VC-1 (decoders: vc1 vc1_qsv vc1_cuvid )
    DEV.L. vp8                  On2 VP8 (decoders: vp8 libvpx vp8_cuvid vp8_qsv ) (encoders: libvpx )
    DEV.L. vp9                  Google VP9 (decoders: vp9 libvpx-vp9 vp9_cuvid vp9_qsv ) (encoders: libvpx-vp9 vp9_qsv )
    ```

3. 视频转码

    ```bash
    ffmpeg -c:v h264 -i 1.mp4  -c:v mpeg4 output.mp4
    ```

    - `-c:v h264` : 指定输入视频解码器为`h264`
    - `-i 1.mp4` : 指定源视频
    - `-c:v mpeg4` : 指定输出视频解码器为`mpeg4`

    ```bash
    ffmpeg -hwaccel cuvid -c:v h264_cuvid -i 1.mp4 -c:v h264_nvenc -b:v 2048k  -y output.mp4
    ```



    - `-hwaccel cuvid`：指定使用`NVIDIA GPU`硬件加速
    - `-c:v h264_cuvid`：使用`h264_cuvid`进行视频解码
    - `-c:v h264_nvenc`：使用`h264_nvenc`进行视频编码

4. 查看原视频的编码方式

    ffprobe工具支持查看文件编码信息

    ```text
    ffprobe 1.mp4

    # 输出
    Input #0, mov,mp4,m4a,3gp,3g2,mj2, from '1.mp4':
    Metadata:
        major_brand     : isom
        minor_version   : 512
        compatible_brands: isomiso2avc1mp41
        encoder         : Lavf58.29.100
    Duration: 00:09:43.59, start: 167.530998, bitrate: 891 kb/s
    Stream #0:0[0x1](und): Video: h264 (High) (avc1 / 0x31637661), yuv420p(tv, bt709, progressive), 1920x1080 [SAR 1:1 DAR 16:9], 755 kb/s, 30 fps, 30 tbr, 15360 tbn (default)
        Metadata:
        handler_name    : ISO Media file produced by Google Inc.
        vendor_id       : [0][0][0][0]
    Stream #0:1[0x2](und): Audio: aac (LC) (mp4a / 0x6134706D), 44100 Hz, stereo, fltp, 128 kb/s (default)
        Metadata:
        handler_name    : ISO Media file produced by Google Inc.
        vendor_id       : [0][0][0][0]
    ```

5. 视频文件抽帧为图片

    ```bash
    ffmpeg -i 1.mp4 -r 30 -f image2 images/foo-%05d.jpg -y

    # 使用GPU加速
    ffmpeg -hwaccel cuvid -c:v h264_cuvid -i regular.mp4 -r 30 -f image2 -c:v h264_nvenc  1123/image_%08d.jpg -y
    ```

    - `-r 30`: 每秒取的帧数,`fps`
    - `-f image2`: 设置输出文件的格式
    - `images/foo-%05d.jpg`: 输出文件的保存地址

6. 合并图片为视频

    生成需要合并的jpg文件列表。打开cmd.exe，改变路径到包含jpg的文件夹，然后运行如下代码，就可以得到一个`mylist.txt`文件，里面会包含所有需要合并的jpg文件的名字。

    ```bat
    (for %i in (*.jpg) do @echo file '%i') > mylist.txt
    ffmpeg -f concat -safe 0 -i mylist.txt -c copy all.mp4
    ```

7. 合并音频与视频

    ```bash
    ffmpeg -i video.m4s -i audio.m4s -codec copy Output.mp4
    ```

8. ffmpeg获取本地音视频设备列表

    ```bash
    ffmpeg -list_devices true -f dshow -i dummy

    # 输出
    [dshow @ 000001ed54281f80] "PC Camera" (video)
    [dshow @ 000001ed54281f80]   Alternative name "@device_pnp_\\?\usb#vid_058f&pid_2657&mi_00#6&395b6ec3&0&0000#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\global"
    [dshow @ 000001ed54281f80] "麦克风 (2- Magic Sound)" (audio)
    [dshow @ 000001ed54281f80]   Alternative name "@device_cm_{33D9A762-90C8-11D0-BD43-00A0C911CE86}\wave_{BD25D5CB-26B4-4A97-9A6F-BD84ED0B4312}"
    [dshow @ 000001ed54281f80] "麦克风 (Realtek(R) Audio)" (audio)
    [dshow @ 000001ed54281f80]   Alternative name "@device_cm_{33D9A762-90C8-11D0-BD43-00A0C911CE86}\wave_{B4B278F2-5292-4EC1-A32F-B79102AD9198}"
    ```

9. ffmpeg播放、保存USB摄像头数据

    ```bash
    # 展示
    ffplay -f dshow -i video="name" -vf scale=640:480
    # 保存
    ffmpeg -f dshow -i video="name" -vf scale=640:480 -vcodec libx264 output.mkv
    ```

    > 注 : 上述`name`为设备列表查询输出信息中`Alternative name`中引号的字符串

10. 调整视频播放速率

    视频的倍速主要是通过控制`filter`中的`setpts`来实现,`setpts`是视频滤波器通过改变每一个`pts`时间戳来实现倍速的效果，如下只要把`PTS`缩小一半就可以实现2倍速，相反的是`PTS`增加一倍就达到2倍慢放的效果。实现：

    ```bash
    ffmpeg -i test.mp4 -an -filter:v "setpts=n*PTS" output.mp4 
    ```

    其中`n`的范围 : `[0.25, 4]`，n越大播放速率越慢。

11. 调整视频分辨率

    ```bash
    ffmpeg -i input.mp4 -vf scale=weight:height -y output.mp4
    ```

    其中weight表示转出视频的宽，height表示转出视频的高，如1920:1080

12. 截取视频段

    ```bash
    ffmpeg -ss 00:00:17 -to 00:00:50 -i input.mp4 -vcodec copy -acodec copy output.mp4
    ```

    表示截取输入视频的 00:00:17到00:00:50这一段

13. 横向拼接
    ```
    ffmpeg -i 1.mp4 -i 2.mp4 -filter_complex hstack output.mp4
    ```
    横向拼接1，2两个视频

14. 分离视频音频流

    ```bash
    # 分离视频流 
    ffmpeg -i 1.mp4 -vcodec copy -an output_file_video　　
    # 分离音频流
    ffmpeg -i 1.mp4 -acodec copy -vn audio.mp4
    ```


15. ffmpeg截取视频片段

    ```bash
    ffmpeg -ss 0:1:30 -t 0:0:20 -i 1.mp4 -vcodec copy -acodec copy output.mp4
    ```

    - -r 提取图像的频率，
    - -ss 开始时间，
    - -t 持续时间

16. ffmpeg从视频中生成gif图片

    ```bash
    ffmpeg -i 1.mp4 -t 10 -vf scale=320:240 -pix_fmt rgb24 jidu1.gif
    ```

    - `-t`参数表示提取前10秒视频
    - `-vf scale=320:240` 表示按照 320x240的像素提取


# 参考链接

- **[简 书]** [使用GPU硬件加速FFmpeg视频转码](https://www.jianshu.com/p/59da3d350488)
- **[CSDN]** [FFMPEG详解(完整版）](https://blog.csdn.net/davidullua/article/details/120562737)
- **[CSDN]** [FFmpeg指令行打开usb摄像头（windows）](https://blog.csdn.net/athrunsunny/article/details/122319491)
- **[知 乎]** [FFMEPG各种操作](https://zhuanlan.zhihu.com/p/391628564)