#!/bin/bash

# 显示帮助信息
function show_help {
  echo "这个脚本用于抽取视频文件中的图片帧。"
  echo "用法: bash extract_frames.sh [-h] /path/to/videos /path/to/output"
  echo "选项："
  echo "  -h, --help    显示帮助信息并退出"
  echo "参数："
  echo "  /path/to/videos    视频文件或包含视频文件的文件夹的路径,文件夹需要以/结尾"
  echo "  /path/to/output    输出图片帧的文件夹路径"
}

# 检查是否有-h或--help选项
while getopts ":h" opt; do
  case ${opt} in
    h )
      show_help
      exit 0
      ;;
    \? )
      echo "无效选项：-$OPTARG" 1>&2
      exit 1
      ;;
  esac
done
shift $((OPTIND -1))

# 输入的视频文件或文件夹路径
input_path=$1
# 输出的图片帧文件夹路径
output_dir=$2
# 设置抽帧的帧率，即每秒抽取多少帧
FPS=2
# 设置输出图片的分辨率，当前为2k分辨率，1080P分辨率为1920x1080，4k分辨率为3840x2160
definition=2560x1440

# 检查输出文件夹是否存在，如果不存在则创建
if [ ! -d "$output_dir" ]; then
  mkdir -p "$output_dir"
fi

# 检查输入路径是文件还是文件夹
if [ -d "$input_path" ]; then
  # 如果是文件夹，遍历文件夹中的每一个文件
  for video_file in "$input_path"/*; do
    base_name=$(basename "$video_file" .mp4)
    echo "正在处理 $video_file..."
    echo "输出到 $output_dir/images_$base_name/..."
    if [ ! -d "$output_dir/images_$base_name" ]; then
      mkdir -p "$output_dir/images_$base_name"
    fi    

    echo "basename: $base_name"
    image_filename_prefix="images_$base_name"
    echo "image_filename_prefix: $image_filename_prefix"
    echo "FPS: $FPS"
    # 变量引用部分不需要加引号，以免被解释为字符串
    ffmpeg -i "$video_file" -r $FPS -s $definition -f image2 $output_dir/"images_"$base_name/$image_filename_prefix"_%10d.png" -y
  done
elif [ -f "$input_path" ]; then
  # 如果是文件，直接处理该文件
  base_name=$(basename "$input_path" .mp4)
  echo "正在处理 $input_path..."
  echo "输出到 $output_dir/images_$base_name/..."
  if [ ! -d "$output_dir/images_$base_name" ]; then
    mkdir -p "$output_dir/images_$base_name"
  fi
  ffmpeg -i "$video_file" -r $FPS -s $definition -f image2 $output_dir/"images_"$base_name/$image_filename_prefix"_%10d.png" -y
else
  echo "输入的路径既不是文件也不是文件夹，请检查后重新输入。"
fi
