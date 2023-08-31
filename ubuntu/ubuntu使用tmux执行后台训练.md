[TOC]

# Tmux 是什么？

## 会话与进程

命令行的典型使用方式是，打开一个`终端窗口(terminal window)`，以下简称`窗口`，在里面输入命令。用户与计算机的这种临时的交互，称为一次`会话(session)`

会话的一个重要特点是，窗口与其中启动的进程是连在一起的。打开窗口，会话开始；关闭窗口，会话结束，会话内部的进程也会随之终止，不管有没有运行完。

一个典型的例子就是，`SSH`登录远程计算机，打开一个远程窗口执行命令。这时，网络突然断线，再次登录的时候，是找不回上一次执行的命令的。因为上一次`SSH`会话已经终止了，里面的进程也随之消失了。

为了解决这个问题，会话与窗口可以**解绑**：窗口关闭时，会话并不终止，而是继续运行，等到以后需要的时候，再让会话**绑定**其他窗口。

## Tmux 的作用

Tmux 就是会话与窗口的"解绑"工具，将它们彻底分离。

1. 它允许在单个窗口中，同时访问多个会话。这对于同时运行多个命令行程序很有用。
2. 它可以让新窗口"接入"已经存在的会话。
3. 它允许每个会话有多个连接窗口，因此可以多人实时共享会话。
4. 它还支持窗口任意的垂直和水平拆分。

# 安装与使用

```bash
sudo apt-get install tmux   # 安装
tmux                        # 进入tmux窗口
exit                        # 推出tmux窗口，或者使用快捷键[ Ctrl+d ]
tmux new -s ${session-name} # 创建一个会话，并设置绘画名
# 快捷键[ Ctrl+b ] 是tmux的前缀键，用完前缀键后可以继续按指定键来完成指定命令
[ Ctrl+b ] [ d ]                         # 将会话与窗口分离，或者[ Ctrl+b ] tmux detach
tmux ls                                  # 查看所有会话，或者使用tmux list-session
tmux attach -t ${session-name}           #  根据会话名将terminal窗口接入会话
tmux kill-session -t ${session-name}     #  根据会话名杀死会话
tmux switch -t ${session-name}           # 根据会话名切换会话
tmux rename-session -t 0 ${session-name} # 根据会话名，重命名会话
```

# 参考链接

- [阮一峰tmux使用教程](https://www.ruanyifeng.com/blog/2019/10/tmux.html)
- [cnblogs](https://www.cnblogs.com/gy77/p/16746769.html)