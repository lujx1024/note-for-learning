---
title: Python小功能脚本合集
tags: Python,功能,脚本
renderNumberedHeading: true
grammar_cjkRuby: true
---

* [概述](#概述)
* [脚本](#脚本)
	* [递归获取所有子文件](#递归获取所有子文件)
	* [python 实现KMP算法](#python-实现kmp算法)

# 概述
本文用于收集编程过程中的常用小功能实现脚本
# 脚本

## 递归获取所有子文件
```
import os
from typing import List

def get_all_files(src_dir:str)->List:
    """
    get all the files within this directory, the files in the sub-directories included

    Args:
        src_dir (str): the path of source directory, absolute path was highly recommanded

    Returns:
        List: return a list of file paths if the parameter is a directory
        if the src_dir is a file, return a list that only contains src_dir as it's member
    """
    files = []
    assert os.path.exists(src_dir),f"current directory or file not exists : {src_dir}"
    # if the src_dir is a file , return a list only contains it
    if os.path.isfile(src_dir):
        return [src_dir]
    
    listFiles = os.listdir(src_dir)
    for i in range(0, len(listFiles)):
        path = os.path.join(src_dir, listFiles[i])
        if os.path.isdir(path):
            files.extend(get_all_files(path))
        elif os.path.isfile(path):
            files.append(path)
    return files
```

## python 实现KMP算法
```
# Python program for KMP Algorithm
def KMPSearch(pat, txt):
	M = len(pat)
	N = len(txt)

	# create lps[] that will hold the longest prefix suffix
	# values for pattern
	lps = [0]*M
	j = 0 # index for pat[]

	# Preprocess the pattern (calculate lps[] array)
	computeLPSArray(pat, M, lps)

	i = 0 # index for txt[]
	while i < N:
		if pat[j] == txt[i]:
			i += 1
			j += 1

		if j == M:
			print ("Found pattern at index", str(i-j))
			j = lps[j-1]

		# mismatch after j matches
		elif i < N and pat[j] != txt[i]:
			# Do not match lps[0..lps[j-1]] characters,
			# they will match anyway
			if j != 0:
				j = lps[j-1]
			else:
				i += 1

def computeLPSArray(pat, M, lps):
	len = 0 # length of the previous longest prefix suffix

	lps[0] # lps[0] is always 0
	i = 1

	# the loop calculates lps[i] for i = 1 to M-1
	while i < M:
		if pat[i]== pat[len]:
			len += 1
			lps[i] = len
			i += 1
		else:
			# This is tricky. Consider the example.
			# AAACAAAA and i = 7. The idea is similar
			# to search step.
			if len != 0:
				len = lps[len-1]

				# Also, note that we do not increment i here
			else:
				lps[i] = 0
				i += 1

txt = "你好，我是奥拓电子，我是..."
pat = "我是"
KMPSearch(pat, txt)
```

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。

