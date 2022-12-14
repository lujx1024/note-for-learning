---
title: 以管理员权限执行bat批处理文件
tags: 管理员权限,批处理
renderNumberedHeading: true
grammar_cjkRuby: true
---

# 概述
使用批处理文件启动或终止某系统服务或软件时，常常需要使用以管理员身份运行BAT脚本文件，这里记录一下以管理员身份运行批处理脚本的两种方式

> 注：在运行之前，需要修改`用户账户控制设置`，将通知设置改为`从不通知`，即将滑块移动至**最下方**，设置路径：`WIN+R组合键`$\rightarrow$`control`$\rightarrow$`系统和安全`$\rightarrow$`安全和维护`$\rightarrow$`更改用户账户控制设置` 
## 批处理指令请求管理员权限
在批处理指令文件的文件头加入以下代码后，即可实现默认以管理员运行：
```
@echo off  
   
:: BatchGotAdmin  
:-------------------------------------  
REM  --> Check for permissions  
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"  
   
REM --> If error flag set, we do not have admin.  
if '%errorlevel%' NEQ '0' (  
 echo Requesting administrative privileges...  
 goto UACPrompt  
) else ( goto gotAdmin )  
   
:UACPrompt  
 echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"  
 echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"  

 "%temp%\getadmin.vbs"  
 exit /B  
   
:gotAdmin  
 if exist "%temp%\getadmin.vbs" ( del "%temp%\getadmin.vbs" )  
 pushd "%CD%"  
 CD /D "%~dp0"  
:-----------------------------

```
## 设置快捷方式默认管理员身份运行
1. 创建批处理文件的快捷方式
鼠标选中批处理文件选择`发送到`$\rightarrow$  `桌面快捷方式` 或`新建`$\rightarrow$ `快捷方式`，将快捷方式的对象位置指向批处理文件即可。

2. 设置快捷方式默认以管理员运行
右击快捷方式选择`属性(properties)`$\rightarrow$`高级(Advanced)`,勾选`以管理员身份运行`即可

## 其他方式
1. 下载`bat转exe工具`，将`bat`转成`exe`,然后右键`exe`选择`属性(properties)`$\rightarrow$`高级(Advanced)`,勾选`以管理员身份运行`即可
2. 以管理员权限运行`cmd`，然后`dos`框中运行相应的`bat`

## 参考链接
- 【51CTO】[BAT-把当前用户以管理员权限运行](https://blog.51cto.com/u_15060549/4669505)
- 【likecs】[如何让bat文件以管理员身份运行](https://www.likecs.com/show-482040.html)


欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。