---
title: Program With Mosh -- Docker Linux基础之环境变量
tags: Docker
category: Mosh/Docker笔记/Linux环境变量
renderNumberedHeading: true
grammar_cjkRuby: true
---

## Linux 指令
### 包管理指令
以编辑软件nano为例，使用ubuntu操作系统安装及卸载软件
- `apt update`
- `apt list`
- `apt install nano`
- `apt remove nano`
 
 ### Searching for text
- `grep hello file.txt`         # 在file.txt中 检索 hello字符串
 - `grep -i hello file.txt`       # 忽略大小写进行字符串检索 
 - `grep -i hello file*.txt`       # 使用正则表达式进行字符串检索
 - `grep -i -r hello` .          # 在当前文件夹中，递归检索
 ### Finding files and directories
 - `find`             # to list all files and directories
 - `find -type d`       # to list directories only
 - `find -type f`       # to list files only
 - `find -name “f*”`    # to filter by name using a pattern
 
### Managing environment variables
- `printenv`         # to list all variables and their value
- `printenv PATH`      # to view the value of PATH
- `echo $PATH`         # to view the value of PATH
- `export name=bob`    # to set a variable in the current session
### Managing processes
- `ps`                 # to list the running processes
- `kill 37`            # to kill the process with ID 37
### Managing users and groups
- `useradd -m john`    # to create a user with a home directory
- `adduser john`       # to add a user interactively
- `usermod`            # to modify a user
- `userdel`            # to delete a user
- `groupadd devs`      # to create a group
- `groups john`        # to view the groups for john
- `groupmod`           # to modify a group
- `groupdel`           # to delete a group

### File permissions
- `chmod u+x deploy.sh`    # give the owning user execute permission
- `chmod g+x deploy.sh`    # give the owning group execute permission
- `chmod o+x deploy.sh`    # give everyone else execute permission
- `chmod ug+x deploy.sh`   # to give the owning user and group execute permission
- `chmod ug-x deploy.sh`   # to remove the execute permission from   the owning user and group 


欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。