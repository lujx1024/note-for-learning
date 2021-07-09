---
title: Python线程间与进程间通讯
tags: 新建,模板,小书匠
renderNumberedHeading: true
grammar_cjkRuby: true
---
# 概述
本篇博客主要记录python程序使用多线程或多进程方法进行运算或其他操作时，主线程或主进程获取子线程或子进程的返回值的方法。不涉及资源锁或信号量等方法的使用。

# 主线程获取子线程的执行返回值
子线程的执行返回值获取方法有很多种，这里记录使用`threading`模块创建的多线程和使用线程池`concurrent.future`模块创建的子线程执行结果获取方法。

## `threading`模块子线程返回值获取

1. 自定义线程类

	继承`threading.Thread`，创建自定义线程类，封装进程执行方法，并自定义方法返回执行结果。
	```
	class MyThread(threading.Thread):
		def __init__(self, func, args=()):
			super(MyThread, self).__init__()
			self.func = func
			self.args = args

		def run(self):
			self.result = self.func(*self.args)

		def get_result(self):
			try:
				return self.result
			except Exception:
				return None
	```

2. 创建自定义对象，传入执行方法和参数，以阻塞式启动子线程，待子线程执行结束后，获取子线程执行结果；
	 ```
	import threading
	import time

	def do_something(seconds: int):
		"""
		线程执行函数，使用sleep函数模拟耗时操作
		Args:
			seconds (int): 睡眠时间代表耗时操作

		"""
		print(f"Sleep {seconds} second(s)...")
		time.sleep(seconds)
		return 'Done Sleeping'

	class MyThread(threading.Thread):
		def __init__(self, func, args=()):
			super(MyThread, self).__init__()
			self.func = func
			self.args = args

		def run(self):
			self.result = self.func(*self.args)

		def get_result(self):
			try:
				return self.result
			except Exception:
				return None

	if __name__ == '__main__':
		thread = MyThread(do_something, args=(1,))
		thread.start()
		thread.join()
		result = thread.get_result()
		print("子线程返回值 :", result)
	```

## 使用`ThreadPoolExecutor`的线程执行结果获取
`python 3.x`内置模块`concurrent.future`,定义了`Executor`抽象类，该抽象类有`ThreadPoolExecutor`和`ProcessPoolExecutor`两个实现类，分别是线程池的和进程池的实现类，进程池后文会详述。

`ThreadPoolExecutor`封装了比较友好的接口用于获取线程执行结果，`concurrent.future`模块定义了`Future`类，用于保存线程或进程执行结果。Future类注释如下：
```
Represents the result of an asynchronous computation.

用于定义异步计算的执行结果
```
使用方法：
```
import time
from concurrent.futures import Future
from concurrent.futures.thread import ThreadPoolExecutor

def do_something(seconds: int):
    """
    线程执行函数，使用sleep函数模拟耗时操作
    Args:
        seconds (int): 睡眠时间代表耗时操作

    """
    print(f"Sleep {seconds} second(s)...")
    time.sleep(seconds)
    return 'Done Sleeping'

if __name__ == '__main__':
    with ThreadPoolExecutor() as executor:
        # 此处 : Future 主要用于标注，可省略
        future: Future = executor.submit(do_something, 1)        
        result = future.result()
        print("线程执行结果", result)
```

# 进程间获取执行返回值
同多线程一样，多进程程序同样有多重实现方式，其中，主要使用`multiprocessing`模块和`concurrent.future`模块，不同的实现方式，有不同的进程间通讯方法，

##  `multiprocessing.Process`对象的进程间通讯

### `multiprocessing.Pipe`消息管道
可以使用`multiprocessing`模块的`Pipe`实现两个`multiprocessing.Process`进程之间的数据传递。`Pipe`本身是一个消息管道。`Pipe`类注释简单粗暴:
```
Returns pair of connection objects at either end of a pipe

Pipe类实例会返回一对分别属于管道两头的连接对象。简单来讲就是，两个进程分别持有管道两头的连接，实现消息在管道中的收发

```
实现示例：
```
import multiprocessing
from multiprocessing.connection import Pipe
import time


def do_something(pipe: Pipe, seconds: int):
    """
    进程执行方法，持有管道连接对象
    Args:
        pipe (multiprocessing.connection.Pipe): 管道连接对象
        seconds (int): 休眠时间，用于线程方法耗时

    """
    print(f"sleeping {seconds} ...")
    time.sleep(seconds)
    print("Done sleeping")
    # 向管道中发送数据
    pipe.send("this msg is send from subprocess")


if __name__ == '__main__':
    # 创建一对管道连接
    conn1, conn2 = Pipe()
    # 创建子进程
    p_1 = multiprocessing.Process(target=do_something, args=(conn1, 1))
    # 以阻塞式方式启动进程
    p_1.start()
    p_1.join()
    # 获取子进程向管道中发送的消息
    result = conn2.recv()
    print("收到子进程的返回值 : ", result)
    exit(0)
```

### `multiprocessing.Queue`消息队列
同样，使用`multiprocessing.queues.Queue`对象可实现多个`multiprocessing.Process`之间的通讯，以安全的`生产者-消费者模式`为例，`生产者进程`向消息队列中推送数据，`消费者进程`从消息队列中获取数据.
```
import multiprocessing
from multiprocessing.connection import Pipe
import time
from multiprocessing.context import Process
from multiprocessing.queues import Queue

def do_something(queue: Queue, seconds: int):
    """
    进程执行方法，持有消息队列对象
    Args:
        pipe (multiprocessing.connection.Pipe): 管道连接对象
        seconds (int): 休眠时间，用于线程方法耗时

    """
    print(f"sleeping {seconds} ...")
    time.sleep(seconds)
    print("Done sleeping")
    # 向管道中发送数据
    queue.put("this msg is send from subprocess")

if __name__ == '__main__':
    # 创建消息队列
    queue = Queue(ctx=multiprocessing.get_context())
    # 创建子进程
    p_1 = Process(target=do_something, args=(queue, 1))
    # 以阻塞式方式实现子进程
    p_1.start()
    p_1.join()

    # 获取消息队列中的子进程返回值
    result = queue.get()
    print("收到子进程的返回值 : ", result)
    exit(0)
```
**以上两种方式所介绍的进程对象均由`multiprocessing.Process`创建，关于线程池创建的对象的数据共享用户进程通信，需要使用`multiprocessing.Manager`进行处理**

## `multiprocessing.Pool`进程池的数据共享与进程通信

### `multiprocessing.Manager`实现数据共享

现有主进程数据对象(列表、字典等)，在使用多进程进行数据处理时，由于进程对象使用的是进程池创建，使用内置`list`或`dict`对象，无法实现进程间数据共享，子进程所做的数据修改，主进程或其他进程也无法获取到。需使用`multiprocessing.Manager`对象创建的`list`或`dict`方可实现。
举例说明，现有主进程数据列表对象，原始数据为空，使用进程池对象创建数个子进程，每个子进程中将进程号保存到主进程的数据列表中，进程池中的所有子进程执行结束后，在主进程中获取所有子进程的子进程编号。代码实现：
```
import multiprocessing
import os
from multiprocessing.connection import Pipe
import time
from multiprocessing.context import Process
from typing import List

def do_something(manager_list: List[int], seconds: int):
    """
    进程执行方法，持有管道连接对象
    Args:
        pipe (multiprocessing.connection.Pipe): 管道连接对象
        seconds (int): 休眠时间，用于线程方法耗时

    """
    print(f"sleeping {seconds} ...")
    time.sleep(seconds)
    print("Done sleeping")
    # 向共享数据中保存进程编号数据
    manager_list.append(os.getpid())

if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        manager_list = manager.list()
        pool = multiprocessing.Pool()

        pool.apply_async(do_something, (manager_list, 2))
        pool.apply_async(do_something, (manager_list, 2))
        pool.close()
        pool.join()
		# 主进程获取子进程编号列表数据
        print(manager_list)
    exit(0)
```

### `multiprocessing.Manager`消息队列实现进程通信
同理，使用`multiprocessing.Manager.Queue`可实现进程池通讯，实现代码如下：
```
import multiprocessing
import os
import time
from queue import Queue

def do_something(manager_queue: Queue, seconds: int):
    """
    进程执行方法，持有管道连接对象
    Args:
        pipe (multiprocessing.connection.Pipe): 管道连接对象
        seconds (int): 休眠时间，用于线程方法耗时

    """
    print(f"sleeping {seconds} ...")
    time.sleep(seconds)
    print("Done sleeping")
    # 向管道中发送数据
    manager_queue.put(f"{os.getpid()} put this message")


if __name__ == '__main__':
    with multiprocessing.Manager() as manager:
        manager_queue = manager.Queue()
        pool = multiprocessing.Pool()

        pool.apply_async(do_something, (manager_queue, 2))
        pool.apply_async(do_something, (manager_queue, 2))
        pool.close()
        pool.join()
        while not manager_queue.empty():
            print(manager_queue.get())
    exit(0)
```


参考连接：
- https://zhuanlan.zhihu.com/p/64702600
- https://www.cnblogs.com/jiangfan95/p/11439207.html
- https://blog.csdn.net/weixin_43790276/article/details/90906683
- http://c.biancheng.net/view/2635.html
- https://www.cnblogs.com/tashanzhishi/p/10775641.html

欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。