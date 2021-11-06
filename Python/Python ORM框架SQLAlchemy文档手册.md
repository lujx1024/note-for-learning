---
title: Python ORM框架SQLAlchemy文档手册
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---

[TOC]

# 概述



# 环境搭建
## 数据库
以`MySQL`数据库为例，数据库`host`位于局域网机器`192.168.1.124`上，数据库驱动使用`pymysql`,开发语言使用`python`

## 数据库驱动及ORM依赖包安装
安装数据库驱动  `pip install pymysql`
安装 ORM  框架 `pip install SQLAlchemy`

# SQLAlchemy的使用

## 数据库连接与SQL语句执行
### 创建连接引擎

任何`SQLAlchemy`应用程序的开始都是一个名为 `Engine `. 此对象充当连接到特定数据库的中心源，提供工厂和称为 `connection pool` 对于这些数据库连接。引擎通常是一个只为特定数据库服务器创建一次的全局对象，并使用一个`URL字符串`进行配置，该字符串将描述如何连接到数据库主机或后端。

```
from sqlalchemy import create_engine, text

# mysql数据库位于192.168.1.124:3306，驱动使用的是pymysql,连接的数据库名是test
db_link = f'mysql+pymysql://username:password@192.168.1.124:3306/test'
engine = create_engine(db_link)
```
上述代码中，`db_link` 作为数据库链接字符串，包含三部分内容：
1. 和什么数据库通信，本实例中，显然是`mysql`
2. 用什么数据库驱动，本实例中，用的是`pymysql`
3. 主机地址、用户名、密码等数据库定位参数

### 获取连接

从用户层面来说，`Engine`对象的唯一目的便是提供一个数据库连接对象，即`Connection`对象，当直接使用 `SQLAlchemy Core`模块时，`Connection`对象负责完成数据库交互工作，由于`Connection`对象表示对数据库的开放资源，我们希望将此对象的使用范围限制在一个上下文范围内，最好的方式便是使用Python上下文管理器，即`with`表达式。下面以`hello world`这个`SQL`语句文本表达式做示例。**SQL文本表达式对象由`text()`这个构造方法生成**.

```
from sqlalchemy import text

with engine.connect() as conn:
    result = conn.execute(text("select 'hello world'"))
    print(result.all())
	
```
代码执行后输出`[('hello world',)]`

### Connection对象执行SQL语句

使用原生SQL创建数据表与数据导入
```
with engine.connect() as conn:
		conn.execute(text("CREATE TABLE some_table (x int, y int)"))
     	conn.execute(text("insert into some_table (x,y) values (:x,:y) "), [{"x": 5, "y": 6}])
```

数据查询
```
with engine.connect() as conn:
    result = conn.execute(text("SELECT x, y FROM some_table"))
    for row in result:
        print(f"x: {row.x}  y: {row.y}")
```

### ORM会话（Session）

上述`Connection`对象中的方法，同样适用于`Session`对象。

使用`Session`对象执行`SQL`原生语句
```
with Session(engine) as session:
    result = session.execute(
        text("insert into some_table (x,y) values (:x,:y) "),
        [{"x": 10, "y": 12}, {"x": 25, "y": 54}]
    )
    session.commit()
```

## 数据库元数据 (MetaData)

### Core 模块定义 MetaData

`MetaData`是`Table`对象的集合，这个对象本质上是一个 facade 在Python字典中存储了一系列 Table 对象键控到其字符串名称。构造此对象的方式如下：
```
from sqlalchemy import MetaData
metadata = MetaData()
```

一旦有了`MetaData`对象后，便可以定义`Table`对象，以用户表`user_table`和地址表`address_table`为例：

```
from sqlalchemy import Table, Column, Integer, String
user_table = Table(
    "user_account",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(30)),
    Column('fullname', String)
)

from sqlalchemy import ForeignKey
address_table = Table(
    "address",
    metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', ForeignKey('user_account.id'), nullable=False),
    Column('email_address', String, nullable=False)
)

```
从上述代码看出，`Table`对象的定义与数据库数据表定义类似，所用到的对象有：
1. `Table` 对应数据表的Python对象，定义时，存储到MetaData对象中
2. `Column` 定义对象属性，对应数据表的列， Column 通常包括一个字符串名和一个类型对象

`Table`对象属性查询
1. 查询列属性
	```
	>>> user_table.c.name
	Column('name', String(length=30), table=<user_account>)

	>>> user_table.c.keys()
	['id', 'name', 'fullname']
	```
2. 查询主键约束
	```
	>>> user_table.primary_key
	PrimaryKeyConstraint(Column('id',Integer(),table=<user_account>, primary_key=True,nullable=False))
	```

在数据库中创建数据表
`metadata.create_all(engine)`

### ORM 模块定义 MetaData

使用`ORM`时 `MetaData `集合仍然存在，但是它本身包含在名为 `registry `的注册表对象中. 我们创建一个 `registry `：
```
from sqlalchemy.orm import registry
mapper_registry = registry()
```
以上 `registry `，在构造时，自动包含 `MetaData `对象，该对象将存储 Table 物体：
```
print(mapper_registry.metadata)
MetaData()
```

### 关系映射对象

此时，不同于定义`Table`对象，可直接定义数据表映射类，在最常见的方法中，每个映射的类都从一个称为`基础声明类`,即`declarative_base` . 我们从 `registry `使用 `registry.generate_base() `方法：

```
Base = mapper_registry.generate_base()

```
另一种定义方法：
```
from sqlalchemy.orm import declarative_base
Base = declarative_base()
```

此时，定义数据表映射类的方法如下：
```
class User(Base):
    __tablename__ = 'user_account'
    metadata = meta_data
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    fullname = Column(String)

    addresses = relationship("Address", back_populates="user")

    def __repr__(self):
       return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = 'address'
    metadata = meta_data

    id = Column(Integer, primary_key=True)
    email_address = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('user_account.id'))

    user = relationship("User", back_populates="addresses")

    def __repr__(self):
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"

```

### `Table`对象反射

为了完成关于使用表元数据的部分，我们将演示在本节开头提到的另一个操作，即`表反射` . `表反射`是指通过读取数据库的当前状态生成 `Table`对象。而在前面的章节中我们已经声明 Table 对象，然后将DDL发送到数据库，反射过程则相反。

```
As an example of reflection, we will create a new Table object which represents the some_table object we created manually in the earlier sections of this document. There are again some varieties of how this is performed, however the most basic is to construct a Table object, given the name of the table and a MetaData collection to which it will belong, then instead of indicating individual Column and Constraint objects, pass it the target Engine using the Table.autoload_with parameter:

```
在本实例中，使用反射，创建一个`Table`对象，对应数据表`some_table`的`Table`类对象，这个对象创建于`本文档1.3章节`,这也有一些不同的执行方式，但是最基础的是构建一个`Table`对象，传入数据表名和其所属的`MetaData`对象，并将`Engine`对象传递给`Table.autoload_with parameter`参数。便可获取对应的`Table`对象。

`some_table = Table("some_table", metadata, autoload_with=engine)`



欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。