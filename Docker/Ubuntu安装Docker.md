
# 卸载旧版本

在安装Docker之前，需要卸载任何冲突的包。

APT提供了Docker包的非官方发行版。在安装Docker Engine之前，您必须卸载这些包。

非官方包需要卸载的有：

- docker.io
- docker-compose
- docker-compose-v2
- docker-doc
- podman-docker

Docker Engine依赖于containerd和runc。Docker Engine将这些依赖项捆绑为一个包：containerd.io。如果您之前安装了containerd或runc，请卸载它们以避免与Docker Engine捆绑的版本发生冲突。

运行以下命令卸载所有冲突的包：

```bash
for pkg in docker.io docker-doc docker-compose docker-compose-v2 podman-docker containerd runc; do sudo apt-get remove $pkg; done
```

apt-get可能会报告您没有安装这些包。

# 安装Docker Engine

## 配置apt仓库

```
# Add Docker's official GPG key:
sudo apt-get update
sudo apt-get install ca-certificates curl
sudo install -m 0755 -d /etc/apt/keyrings
sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
sudo chmod a+r /etc/apt/keyrings/docker.asc

# Add the repository to Apt sources:
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/ubuntu \
  $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | \
  sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt-get update
```

## 安装最新版docker

```
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

## 安装指定版本docker

查看当前可安装版本：
```
# List the available versions:
apt-cache madison docker-ce | awk '{ print $3 }'

5:24.0.0-1~ubuntu.22.04~jammy
5:23.0.6-1~ubuntu.22.04~jammy
...
```

安装指定版本：
```
VERSION_STRING=5:24.0.0-1~ubuntu.22.04~jammy
sudo apt-get install docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-buildx-plugin docker-compose-plugin
```

## docker环境校验
    
```
sudo docker run hello-world
```