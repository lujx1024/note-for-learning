# 概述

Python中有一个基础的数据结构，叫做元组（**tuple**），但是一般挺少有人会到到它的，因为基本上在开发过程中，列表（**list**）已经能够满足我们的基本需求了。

即使是这样，你也千万不要就此认为元组是多余的。不然在面试被人问，元组和列表有啥区别？为什么需要元组？你就懵了。

在这里，小明总结了以下两点，第一点是大家所熟知的，而第二点可能只有老司机才会知道，而只有学习了第二点，才算真正理解了元组存在的价值和意义。


## 1. 不可变列表

这是`元组`区别于`列表`最显著的特征。

- ==list #009688==：可变的序列

- ==tuple #009688==：不可变的序列

那什么是不可变的序列呢？

那就是在元组对象生成后，诸如列表的`插入元素`、`删除元素`、`添加元素`、`清空元素`、`修改元素`等方法，在元组中通通没有，你无法对其进行`修改`、`删除`，你只能`获取`。

由于元组是不可变的，所以其方法也是很有限的。这里罗列一下。

```
# s1和s2都是元组
s1=(1,2,3)
s2=(4,5,6)

# 拼接生成新元组
s1+s2
s1.__add__(s2)

# 是否包含
2 in s1
s1.__contains__(2)

# 统计元素包含的次数
s1.count(2)

# 获取元素
s1[0]
s1.__getitem__(0)

# 找到2第一次出现的索引
s1.index(2)

# 获取长度
len(s1)

# 重复拼接
s1*n
```

## 2. 具名元组

这个特性，我个人认为，才是元组存在的意义所在。

只讲 `具名元组`，可能不太好理解。如果称之为 `带字段名的记录`，你可能就清楚了。

这里举个例子，但是实现带字段名，需要一个库（**collections**）的支持，你需要导入它。**namedtuple**是一个工厂函数。
```
from collections import namedtuple

# 生成一个City类
City = namedtuple("City", "name country polulation coordinates")
# 实例化
tokyo = City("Tokyo", 'Japan', '36.93', ('35.68','139,69'))

print(tokyo)
# City(name='Tokyo', country='JP', polulation='36.93', coordinates=('35.68', '139,69'))

print(tokyo.name)
# Tokyo
```

看着有点像字典，是不是，可惜他不是字典（获取数值的方法也与字典不同），字典是可变。元组在创建后，就无法再对其进行修改。这在也说明元组适合存放那些无需修改的数据。比如上面的，地名，国家，经纬度。

除了上面的用法之处，这里还要介绍一些元组自己专有的属性。
```
# 打印字段名
print(City._fields)
('name', 'country', 'polulation', 'coordinates')

# 生成新实例
LatLong = namedtuple('LatLong', 'lat long')
Xiamen_tuple = ('Xiemen', 'China', '40,54', LatLong(24.26,118.03))
Xiamen = City._make(Xiamen_tuple)

print(Xiamen)
# City(name='Xiemen', country='China', polulation='40,54', coordinates=(24.26, 118.03))

# 将具名元组转为OrderDict
Xiamen_dict = Xiamen._asdict()
print(Xiamen_dict)
# OrderedDict([('name', 'Xiemen'),('country', 'China'),('polulation','40,54'),('coordinates', LatLong(lat=24.26,long=118.03))])
```

总结一下，元组是一种很强大的可以当作记录来用的数据类型，这才是他存在的价值和意义所在。而为人所熟知的，它的第二个角色才是充当一个不可变的列表。