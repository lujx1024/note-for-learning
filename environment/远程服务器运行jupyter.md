[TOC]
# 概述

对于需要快速创建原型和迭代代码的数据科学家和软件工程师来说，`Jupyter Notebooks`是一个很有价值的工具。但是，在本地机器上运行笔记本可能会受到计算资源和可访问性方面的限制。从远程服务器运行`Jupyter Notebooks`可以帮助克服这些限制，并提供协作和版本控制等额外好处。

在本文中，我们将讨论如何使用脚本从远程服务器运行`Jupyter Notebooks`。这将允许您访问远程服务器的计算能力，并在任何地方与互联网连接的`Jupyter`笔记本上工作。

## 先决条件

开始执行之前,需要先确保满足以下几个条件:

- 远程主机已安装`Jupyter Notebook`
- 可使用`SSH`访问远程主机
- 本地主机具有终端或命令行程序

> 注意: 本文中的所有命令都是在远程主机`Ubuntu 20.04`上测试的。如果您使用的是不同的操作系统，请确保您的命令与您的操作系统兼容。

## 步骤1 — 连接到远程服务器

使用`ssh`连接到远程服务器，指令如下:

```bash
ssh username@remote_host
```

> 注意: 请将`username`和`remote_host`替换为您的用户名和远程主机的IP地址或域名。

## 步骤2 — 创建一个新的`Jupyter Notebook`

在远程服务器上创建一个新的`Jupyter Notebook`，指令如下:

```bash
jupyter notebook --no-browser --port 8888 --allow-root
```
指令启动会输出如下:

```bash
(ml) root@rtx2060:~# jupyter notebook --no-browser --port 8888 --allow-root
[W 09:58:04.494 NotebookApp] Loading JupyterLab as a classic notebook (v6) extension.
[W 2023-08-31 09:58:04.496 LabApp] 'port' has moved from NotebookApp to ServerApp. This config will be passed to ServerApp. Be sure to update your config before our next release.
[W 2023-08-31 09:58:04.496 LabApp] 'port' has moved from NotebookApp to ServerApp. This config will be passed to ServerApp. Be sure to update your config before our next release.
[W 2023-08-31 09:58:04.496 LabApp] 'allow_root' has moved from NotebookApp to ServerApp. This config will be passed to ServerApp. Be sure to update your config before our next release.
[W 2023-08-31 09:58:04.496 LabApp] 'allow_root' has moved from NotebookApp to ServerApp. This config will be passed to ServerApp. Be sure to update your config before our next release.
[I 2023-08-31 09:58:04.499 LabApp] JupyterLab extension loaded from /root/miniconda3/envs/ml/lib/python3.9/site-packages/jupyterlab
[I 2023-08-31 09:58:04.499 LabApp] JupyterLab application directory is /root/miniconda3/envs/ml/share/jupyter/lab
[I 09:58:04.502 NotebookApp] Serving notebooks from local directory: /root
[I 09:58:04.502 NotebookApp] Jupyter Notebook 6.5.2 is running at:
[I 09:58:04.502 NotebookApp] http://localhost:8888/?token=58ee50c5341a41c62d746a1cdc793fac0d4983e6308becac
[I 09:58:04.503 NotebookApp]  or http://127.0.0.1:8888/?token=58ee50c5341a41c62d746a1cdc793fac0d4983e6308becac
[I 09:58:04.503 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).
[C 09:58:04.505 NotebookApp]

    To access the notebook, open this file in a browser:
        file:///root/.local/share/jupyter/runtime/nbserver-419705-open.html
    Or copy and paste one of these URLs:
        http://localhost:8888/?token=58ee50c5341a41c62d746a1cdc793fac0d4983e6308becac
     or http://127.0.0.1:8888/?token=58ee50c5341a41c62d746a1cdc793fac0d4983e6308becac

```

## 步骤3 — 在本地主机上创建一个新的`SSH`隧道

在本地主机上创建一个新的`SSH`隧道，指令如下:

```bash
ssh -N -f -L localhost:8888:localhost:8888 username@remote_server_ip
```

## 步骤4 — 在本地主机上打开`Jupyter Notebook`

在本地主机上打开`Jupyter Notebook`，指令如下:

```bash
http://localhost:8888/?token=58ee50c5341a41c62d746a1cdc793fac0d4983e6308becac
```
> 注意: 直接复制远程主机启动后，输出的完整`URL`，然后在本地主机上打开浏览器，粘贴`URL`，即可打开`Jupyter Notebook`。

# 参考链接
- [saturncloud](https://saturncloud.io/blog/how-to-run-jupyter-notebooks-from-a-remote-server/)