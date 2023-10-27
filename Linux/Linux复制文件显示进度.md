[TOC]

# 概述

`rsync` 是一个常用的`Linux`应用程序，用于文件同步。

它可以在`本地计算机`与`远程计算机`之间，或者`两个本地目录`之间同步文件（**但不支持两台远程计算机之间的同步**）。它也可以当作文件复制工具，替代`cp`和`mv`命令。

它名称里面的**r**指的是`remote`，`rsync`其
实就是"远程同步"（`remote sync`）的意思。与其他文件传输工具（如 `FTP` 或 `scp`）不同，`rsync`的最大特点是会检查发送方和接收方已有的文件，**仅传输有变动的部分**（默认规则是文件大小或修改时间有变动）。

# 安装

使用前先确认机器是否支持`rsync`，如果没有安装，可以使用以下命令安装：

```shell
# Ubuntu
sudo apt-get install rsync

# CentOS
sudo yum install rsync
```

> 注: 文件传输双方都需要支持或安装`rsync`。


# 基础用法

## 1.本地复制

本机使用`rsync`命令时，可以作为`cp`和`mv`命令的替代方法，将`源目录`同步到`目标目录`。

```shell
rsync -avh --progress  source destination
```

- `-a`：归档模式，表示以递归方式传输文件，保留软链接、文件权限、修改时间戳、属主、属组、设备文件、特殊文件等文件属性，等于`-rlptgoD`，最常用的选项。
- `-v`：详细模式，输出详细信息。
- `-h`：人性化显示，以更易读的方式显示输出信息。
- `--progress`：显示传输过程。

> 注：多个source目录之间用空格分隔，如 `rsync -avh --progress  source1  source2 destination`

目标目录`destination`如果不存在，`rsync`会自动创建。执行上面的命令后，源目录`source`被完整地复制到了目标目录`destination`下面，即形成了`destination/source`的目录结构。

如果只想同步源目录`source`里面的**子文件**或**子文件**夹到目标目录`destination`，则需要在源目录后面加上斜杠`/`

```shell
rsync -avh --progress  source/ destination
```

## 2.模拟复制

如果不确定`rsync`执行后会产生什么结果，可以先用`-n`或`--dry-run`参数进行复制文件的模拟，并不真正执行复制操作。

```shell
rsync -avhn --progress source destination
```

## 3.远程复制

`rsync`还可以在本地机器和远程机器之间同步文件，需要在命令中指定远程机器的用户名和IP地址。

```shell
rsync -avh --progress source username@remote_ip:destination
```

> 注：远程机器需要安装`rsync`，并且开启`ssh`服务。

同样，`rsync`也可以从远程机器复制文件到本地机器。

```shell
rsync -avh --progress username@remote_ip:source destination
```

## 4.`exclude`和`include`参数

### `exclude`参数

有时，我们希望同步时排除某些文件或目录，这时可以用`--exclude`参数指定排除模式。

```shell
rsync -avh --exclude='*.txt' source/ destination
# 或者
rsync -avh --exclude '*.txt' source/ destination
```

上面命令排除了所有`TXT`文件。

> 注: rsync 会同步以"点"开头的隐藏文件，如果要排除隐藏文件，可以这样写`--exclude=".*"`

如果要排除某个目录里面的所有文件，但不希望排除目录本身，可以写成下面这样。

```shell
rsync -avh --exclude 'dir1/*' source/ destination
```

多个排除模式，可以用多个`--exclude`参数。

```shell
rsync -av --exclude 'file1.txt' --exclude 'dir1/*' source/ destination
```

多个排除模式也可以利用`Bash`的大扩号的扩展功能，只用一个`--exclude`参数。

```shell
rsync -av --exclude={'file1.txt','dir1/*'} source/ destination
```

如果排除模式很多，可以将它们写入一个文件，每个模式一行，然后用`--exclude-from`参数指定这个文件。

```shell
rsync -av --exclude-from='exclude-file.txt' source/ destination
```

### `include`参数

`--include`参数用来指定必须同步的文件模式，往往与`--exclude`**结合使用**。

```shell
rsync -avh --include="*.txt" --exclude='*' source/ destination
```

上面命令指定同步时，排除所有文件，但是会包括`TXT`文件



# 参考链接

- [阮一峰的网络日志](https://www.ruanyifeng.com/blog/2020/08/rsync.html)
- [CSDN](https://blog.csdn.net/yspg_217/article/details/122326503)


