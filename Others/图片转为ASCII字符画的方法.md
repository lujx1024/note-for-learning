---
title: 图片转为ASCII字符画的方法 
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---

# 概述
字符画是一系列字符的组合，我们可以把字符看作是比较大块的像素，一个字符能表现一种颜色（暂且这么理解吧），字符的种类越多，可以表现的颜色也越多，图片也会更有层次感。

问题来了，我们是要转换一张彩色的图片，这么多的颜色，要怎么对应到单色的字符画上去？这里就要介绍灰度值的概念了。

灰度值：指黑白图像中点的颜色深度，范围一般从0到255，白色为255，黑色为0，故黑白图片也称灰度图像

我们可以使用灰度值公式将像素的 RGB 值映射到灰度值：
```
gray ＝ 0.2126 * r + 0.7152 * g + 0.0722 * b
```

# 实现方法

```
from PIL import Image
import argparse

# 命令行输入参数处理
parser = argparse.ArgumentParser()

# 输入文件， 输出文件， 输出字符画宽， 输出字符画高
parser.add_argument('file')
parser.add_argument('-o', '--output')
# 不同尺寸的图片转ASCII时，需要根据实际情况调整默认宽与高
parser.add_argument('--width', type=int, default=150)
parser.add_argument('--height', type=int, default=80)

# 获取参数
args = parser.parse_args()

IMG = args.file
WIDTH = args.width
HEIGHT = args.height
OUTPUT = args.output

ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")


# 将256灰度映射到70个字符上
def get_char(r, g, b, alpha=256):
    if alpha == 0:
        return ' '
    length = len(ascii_char)
    gray = int(0.2126 * r + 0.7152 * g + 0.0722 * b)

    unit = (256.0 + 1)/length
    return ascii_char[int(gray/unit)]


if __name__ == "__main__":
    im = Image.open(IMG)
    im = im.resize((WIDTH, HEIGHT), Image.NEAREST)

    txt = ''

    for i in range(HEIGHT):
        for j in range(WIDTH):
            txt += get_char(*im.getpixel((j,i)))
        txt += '\n'

    print(txt)

    # 字符画输出到文件
    if OUTPUT:
        with open(OUTPUT, 'w') as f:
            f.write(txt)
    else:
        with open('output.txt', 'w') as f:
            f.write(txt)

```

# 操作示例
脚本使用方法:
```
# 安装环境
pip install Pillow

# photo.png 是图片文件，建议使用png背景透明的图片
python3 ascii.py photo.png
```

1. 飞桨Logo

![PaddlePaddle](./images/1.jpeg)
输出:
```
                      `..`^.               ."...
                      .cmdd'              .~0qp^
                       wppqO'            `'pqppZ.
                     .'ikZw.              ..abO      .......  .`    ,.."`.'' .^  .Il...^..
            .......  ...'' .   .......   ..  ^.'      .pppppppp.` .+pb . qp`}dm"cmmdpqkp"
            `~qqpI ':mqqpp-"'. . .pppn...qqObq; ..   `......pq'`.'^dk'. :'Zqqqmqm.""^"hq..
          ...bppz .^obkqwOwd  .'.bqdb'. obbpbwbb..        'bp?Cqaqk*.^   ^":dqm..bqq.bbq'.
          .'Ydpd,  '.' ."Xmpq .'pdpp  ''`''.^kpqa.        mqd}mmQ\'`"....<aZkqm.' Cabb).'
          .<qdw>'       .'qqq` .pwp^.       ..dqw`        dq.okk'..   ..iwb.?hwmdqh0I` .
''   ..  . qbpJ' ..   ... pdZ..dppk ..   .. .^dpq.     '.kZ_. oph ... ^' '...  bdn....'''.
'.''''''''hbdb'  ......:cqdqQ.wppp"'.......`bmppx^      Op0^  .>aqw01>. ?qwwwqqdqkppqqpq..
'npqqqqqqqqpw..pqqqqqqqqqdb].-mqd,^pqqqqqqqpqmq!.    '.+wq^^  ...'mhdq^..' 'rnnbpnxv<.
^bkkkkkhbpppm"obakkkkkkkZ!:^'pddu`QbkkkkkkkhQ^^".      ZmY''...  '..'. ..'`Jqp'bpn.db)''.
`.   ...kbq#`'...  ...... '.0ppd'........    '.       'qpbdpwwqqqwwwww^.[pbq]``bpu.'Xqdw.
       Jdpw..              ?mpq>'                     ..":!!!!lll!!iii^^!!^.. .L0f..  '>..
     ..obq..             .:wpw[                        '...............'`.. '  .^   ...'
    .'pbpb.'            ^`pdpw'                       .
  ..'wdbb..             'xdpm.'                      ..                                  .
  '.fqwp`.             .;qpq)                        ..                                  .
  ',{}}? .            ..)})1".                       '' .  ..      ...`'        . ..
```


2. TF

![TF Logo](./images/2_3.png)
输出：

```
                     ;/\  \\+'
                 ,(////\  \\||||>
             i/tt//////\  \\|||||(((_.
         `]fffttt//////\  \\|||||(((()){:
     .;jjfffffttt//////\  \\|||||(((())))))i'
  "(jjjjjfffffttt//////\  \\|||||(((())))))111{I
  }jjjjjjfffffttt//////\  \\|||||(((())))))1111{
$ }jjjjjjfffff}{t//////\  \\|||||((>)))))))1111{
$ }jjjjjjft:   {t//////\  \\|||||((   .})))1111{
$ }jjjj['      {t//////\  \\|||||((       l1111{
$ 1t"          {t//////\  \\|||||(((<        .?{
$              {t//////\  \\|||||(((())]"
               {t//////\  \\|||||(((())))
               {t//////\  \\|||||(((())))
               {t//////\  \\|||||(((())))
               {t//////\  \\|||||((  :[))
               {t//////\  \\|||||((
               {t//////\  \\|||||((
               {t//////\  \\|||||((
               {t//////\  \\|||||((
               {t//////\  \\|||||((
               ;)//////\  \\|||||)<
                   .[//\  \\|)^
                       ;  ~'
```

![TF Logo](./images/2_2.png)
输出：
```
CLLLLLLL1                                 CLLLLLL 0{
0OOOOOOO(                                 0OOOOOO O{
   _O                                     0O      O{
   _O   >OOO   OiOOO`  QOOO   ,OOO)  OOOO 0O      O{  xOOO  OO  LO  1O
   _O  "OL;OO  OO}+OO nO:^OO .OO;JO` OOOQ 0O      O{ JOrIOO CO  OO  OO
   _O  OO   O` Or  OO OO  i> OO   OO OO   0OOOOO  O{ OO   O] O  OO/ O0
   _O  OOXXXO{ Oj  OO :OOr   OO   0O OO   0Ovvvv  O{ O1   OO O-+OCO O`
   _O  OOQQQQ) Oj  OO  'QOO0 OO   LO OO   0O      O{ O_   OO OOOU O'O
   _O  OO      Oj  OO 1?  CO OO   OO OO   0O      O{ OO   O1 nOO  OQO
   _O  uOx  O  Oj  OO OO  OO >Ox IO? OO   0O      O{ OO' CO   OO  OOO
   _O   COOOQ  Oj  OO  OOOO<  cOOOO  OO   0O      O{  OOOO:   OO  ,O.
```

# 参考链接

- [Python 图片转字符画](https://www.ahhhhfs.com/2462/)
- [背景移除工具](https://github.com/danielgatis/rembg)

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。