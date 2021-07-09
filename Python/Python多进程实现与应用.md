---
title: Python多进程实现与应用
tags: Python,多进程,进程池
renderNumberedHeading: true
grammar_cjkRuby: true
---

[TOC]

# Python 多进程模块

`Python`中的多进程是通过`multiprocessing`包来实现的，和多线程的`threading.Thread`差不多，它可以利用`multiprocessing.Process`对象来创建一个进程对象。这个进程对象的方法和线程对象的方法差不多也有`start()`, `run()`,` join()`等方法，其中有一个方法不同`Thread`线程对象中的守护线程方法是`setDeamon`，而`Process`进程对象的守护进程是通过设置`daemon`属性来完成的。

**注： 在Windows上要想使用进程模块，就必须把有关进程的代码写在当前.py文件的if __name__ == ‘__main__’ :语句的下面，才能正常使用Windows下的进程模块。Unix/Linux下则不需要**
# Python 多进程的实现


## `multiprocessing`模块


### 使用`Process`对象创建线程

```
import os
import time
from multiprocessing import Pool

def do_something(seconds):
    print(f'{os.getpid()} Sleeping {seconds} sencond')
    time.sleep(seconds)
    print(f'{os.getpid()} Done sleeping for {seconds}')


if __name__ == '__main__':
    start_time = time.perf_counter()

    # 创建进程对象，args 是进程执行方法 target 的参数，以元组形式传入
    process = Process(target=do_something, args=(1,))
    # 启动进程
    process.start()
    # 阻塞进程，等待子进程结束
    process.join()

    finish_time = time.perf_counter()
    print(f"Finished in {round(finish_time - start_time, 2)} second(s)")
```
### 继承`Process`对象创建线程
与使用继承方式创建自定义线程对象类似，多进程同样可继承`multiprocessing.context `模块的`Process`对象，自定义进程对象，实现方法如下

```
import os
import time
from multiprocessing import Pool

def do_something(seconds):
    print(f'{os.getpid()} Sleeping {seconds} sencond')
    time.sleep(seconds)
    print(f'{os.getpid()} Done sleeping for {seconds}')


class MyProcess(Process):
    def __init__(self, tartget, args=()):
        super(MyProcess, self).__init__()
        self.target = tartget
        self.args = args

    def run(self, *args):
        self.result = self.target(*self.args)


if __name__ == '__main__':
    start_time = time.perf_counter()

    # 创建进程对象，args 是进程执行方法 target 的参数，以元组形式传入
    process = MyProcess(tartget=do_something, args=(1,))
    # 启动进程
    process.start()
    # 阻塞进程，等待子进程结束
    process.join()
    finish_time = time.perf_counter()
    print(f"Finished in {round(finish_time - start_time, 2)} second(s)")
```

### `Process`的其他方法

- 构造方法

```
Process([group [, target [, name [, args [, kwargs]]]]])
　　group: 线程组 
　　target: 要执行的方法
　　name: 进程名
　　args/kwargs: 要传入方法的参数
```
- 实例方法
```
　is_alive()->bool : 返回进程是否在运行
　join([timeout]):阻塞当前上下文环境的进程，直到调用此方法的子进程终止或到达指定的timeout（可选参数）。
　start() : 进程准备就绪，等待CPU调度
　run() : strat()调用run方法，如果实例进程时未制定传入target，这star执行t默认run()方法。
　terminate()：不管任务是否完成，立即停止工作进程
```
- 属性
```
　daemon : 和线程的setDeamon功能一样
　name   :   进程名字
　pid    :    进程号
```
# 进程池的使用
## `multiprocessing`模块

### 使用`Pool`进程池

```
import os
import time
from multiprocessing import Pool

def do_something(seconds):
    print(f'{os.getpid()} Sleeping {seconds} sencond')
    time.sleep(seconds)
    print(f'{os.getpid()} Done sleeping for {seconds}')


if __name__ == '__main__':
    start_time = time.perf_counter()

    # 创建进程数为4的线程池
    pool = Pool(processes=4)

    # 添加进程对象至进程池并异步执行，同步执行调用方法 apply()
    for i in range(4):
        pool.apply_async(do_something, args=(1,))
    # 关闭进程池，不再添加新的进程
    pool.close()
    # 阻塞主进程直至进程池中的所有进程执行完毕
    pool.join()

    finish_time = time.perf_counter()
    print(f"Finished in {round(finish_time - start_time, 2)} second(s)")
```

### `Pool`API 接口

1. `apply()`
   函数原型：apply(func[, args=()[, kwds={}]])
   该函数用于传递不定参数，同python中的apply函数一致，主进程会被阻塞直到函数执行结束（不建议使用，并且3.x以后不再出现）
2. `apply_async()`
  函数原型 `apply_async(func[, args=()[, kwds={}[, callback=None]]])`
  与apply用法一致，但它是非阻塞的且支持结果返回后进行回调
3. `map()`
   函数原型：`map(func, iterable[, chunksize=None])`
   Pool类中的map方法，与内置的map函数用法行为基本一致，它会使进程阻塞直到结果返回
   注意：虽然第二个参数是一个迭代器，但在实际使用中，必须在整个队列都就绪后，程序才会运行子进程
4. `map_async()`
   函数原型：`map_async(func, iterable[, chunksize[, callback]])`
   与map用法一致，但是它是非阻塞的
5. `close()`
   关闭进程池（`pool`），使其不再接受新的任务
6. `terminal()`
   结束工作进程，不再处理未处理的任务
7. `join()`
   主进程阻塞等待子进程的退出， `join`方法要在`close`或`terminate`之后使用

### `Pool`的`apply()`与`apply_async()`的使用与区别

如上述 API 接口介绍所属，apply()是同步式的执行进程，即当前进程完成或终止后，继续执行下一个进程，代码如下所示(==为节省篇幅，省略了部分方法实现 #4CAF50==):

```
import os
import time
from multiprocessing import Pool

if __name__ == '__main__':
    start_time = time.perf_counter()
    # 创建进程数为4的线程池
    pool = Pool(processes=4)
    # 添加进程对象至进程池并异步执行，同步执行调用方法 apply()
    for i in range(4):
        pool.apply(do_something, args=(1,)) # 此处do_something方法同上
    # 关闭进程池，不再添加新的进程
    pool.close()
    # 阻塞主进程直至进程池中的所有进程执行完毕
    pool.join()
    finish_time = time.perf_counter()
    print(f"Finished in {round(finish_time - start_time, 2)} second(s)")
```
函数执行结果如下所示，从输出结果可知，多个进程是按照顺序依次阻塞式执行，即同步执行,每个进程耗时约1秒，总耗时超过4秒：
```
13280 Sleeping 1 sencond
13280 Done sleeping for 1
12660 Sleeping 1 sencond
12660 Done sleeping for 1
15200 Sleeping 1 sencond
15200 Done sleeping for 1
14500 Sleeping 1 sencond
14500 Done sleeping for 1
Finished in 4.2 second(s)

```
使用`apply_async()`方法执行结果如下(代码秩序改动一个地方，即将原`apply()`改为`apply_async()`即可)的结果输出如下,多个进程同时开始，总耗时约为1秒，与单一进程的耗时基金相同，可知此方式为非阻塞式，即异步执行方式：

```
14408 Sleeping 1 sencond
12872 Sleeping 1 sencond
5280 Sleeping 1 sencond
12440 Sleeping 1 sencond
14408 Done sleeping for 1
12872 Done sleeping for 1
5280 Done sleeping for 1
12440 Done sleeping for 1
Finished in 1.19 second(s)
```

###  `Pool`的`map()`与`map_async()`方法的使用

`Pool`对象的`map()`方法与`Python`	内置方法`map()`使用方法类似，依次传入可迭代对象成员作为进程执行方法作为参数，创建进程对象放置在进程池，并阻塞主进程直至进程池中所有的进程全部执行结束或终止。


```
import os
import time
from multiprocessing.pool import Pool

if __name__ == '__main__':
    start_time = time.perf_counter()
    # 创建进程数为4的线程池
    pool = Pool(processes=4)

    # 创建参数列表，用于不同进程的执行方法
    sleep_seconds = [1, 2, 3, 4]

    # map方法依次将可迭代对象的成员作为参数传入进程执行方法
    pool.map(do_something, sleep_seconds)

    # 关闭进程池，不再添加新的进程
    pool.close()
    # 阻塞主进程直至进程池中的所有进程执行完毕
    pool.join()
    finish_time = time.perf_counter()
    print(f"Finished in {round(finish_time - start_time, 2)} second(s)")
```

上述代码的执行结果: 
![enter description here](./images/123_1.gif)

`map_async()`方法使用方法与`map()`，见名知意，`map()`为同步式，`map_async()`为异步式。


## `concurrent.futures`模块
`concurrent.futures`模块同样提供了进程池类`ProcessPoolExecutor`,与`ThreadPoolExecutor`一样继承自抽象类`concurrent.futures.Executor`，二者实现了同样的诸如`submit()`、`map()`、`result()`等方法。

### `ProcessPoolExecutor`进程池

基础实现:

```
import os
import time
from concurrent.futures.process import ProcessPoolExecutor

def do_something(seconds):
    print(f'{os.getpid()} Sleeping {seconds} sencond')
    time.sleep(seconds)
    return f'{os.getpid()} Done sleeping for {seconds}'


if __name__ == '__main__':
    start_time = time.perf_counter()

    # 使用上下文管理器，创建进程池对象
    with ProcessPoolExecutor() as executor:
        # 创建两个进程对象，放入进程池，submit默认阻塞主进程至进程池中的所有进程完成或终止
        future = executor.submit(do_something, 1)
        future2 = executor.submit(do_something, 1)
        
        # 获取进程方法中的返回值
        print(future.result())
        print(future2.result())

    finish_time = time.perf_counter()
    print(f"Finished in {round(finish_time - start_time, 2)} second(s)")
```
### `ProcessPoolExecutor` API 接口
1. `submit()`
   函数原型 : `submit(self, fn, *args, **kwargs)`
   在进程池中创建一个进程，执行函数fn，args为fn的参数，返回执行结果Furture
2. ` map()`
    函数原型 : `map(self, fn, *iterables, timeout=None, chunksize=1)`
	使用方法与`python`内置·方法类似，传入进程执行方法与可迭代对象，作为执行方法的参数依次将每个成员传入进程执行方法，创建进程。并放入进程池管理.
3. `shutdown()`
   函数原型 : `shutdown(self, wait=True)`
   清理进程池资源，可多次调用而不会出现异常，此方法一旦调用，其他进程池实现方法不可用
   wait参数默认为True，表示线程池会一直等待池中的进程对象全部执行结束或终止，系统资源全部回收后，关闭进程池对象
4. `as_completed()`
   函数原型 : `as_completed(fs, timeout=None)`
   等待进程池中的所有进程执行完毕后，生成所有进程执行结果的可迭代对象迭代器

### `submit()`和`as_completed()`的使用

使用方法如下：
```
import os
import time
from concurrent.futures._base import as_completed
from concurrent.futures.process import ProcessPoolExecutor

if __name__ == '__main__':
    start_time = time.perf_counter()

    # 使用上下文管理器，创建进程池对象
    with ProcessPoolExecutor() as executor:
        # 批量创建进程，使用列表生成式放置Future对象
        futures = [executor.submit(do_something, 1) for _ in range(4)]
        
        # 遍历进程执行结果，获取执行结果
        for future in as_completed(futures):
            print(future.result())

    finish_time = time.perf_counter()
    print(f"Finished in {round(finish_time - start_time, 2)} second(s)")
```


### `map()`的使用

`ProcessPoolExecutor`类的实现方法`map()`与`multiprocess.Process`的同名方法用法相同，传入进程执行方法与一个可迭代对象，可迭代对象成员作为进程执行方法的参数，依次传入后创建进程对象，并传入进程池管理，阻塞当前主进程，待进程池中的所有进程执行结束或终止后，继续执行主进程，示例代码如下：

```
import os
import time
from concurrent.futures.process import ProcessPoolExecutor

if __name__ == '__main__':
    start_time = time.perf_counter()

    # 使用上下文管理器，创建进程池对象
    with ProcessPoolExecutor() as executor:
        # 进程执行方法参数列表
        sleep_seconds = [1, 2, 3, 4]

        # 依次传入可迭代对象成员作为进程执行方法参数，创建进程，有进程池管理
        results = executor.map(do_something, sleep_seconds)
        
        # 阻塞，等待进程池中的所有进程执行结束后，迭代执行结果
        for result in results:
            print(result)

    finish_time = time.perf_counter()
    print(f"Finished in {round(finish_time - start_time, 2)} second(s)")
```
执行结果：
![enter description here](./images/456.gif)


```
# -*- coding: UTF-8 -*-
import multiprocessing
import time
import concurrent.futures


def do_something(seconds):
    print(f'Sleeping {seconds} sencond')
    time.sleep(seconds)
    return 'Done sleep'


if __name__ == '__main__':
    start_time = time.perf_counter()

    # processes = []
    # for _ in range(4):
    #     p = multiprocessing.Process(target=do_something, args=(1.5,))
    #     p.start()
    #     processes.append(p)
    # for process in processes:
    #     process.join()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        future = executor.submit(do_something, 1)
        future2 = executor.submit(do_something, 1)
        print(future.result())
        print(future2.result())

    finish_time = time.perf_counter()
    print(f"Finished in {round(finish_time - start_time, 2)} second(s)")
```

```
# -*- coding: UTF-8 -*-
import multiprocessing
import time
import concurrent.futures
from concurrent.futures._base import as_completed


def do_something(seconds):
    print(f'Sleeping {seconds} sencond')
    time.sleep(seconds)
    return 'Done sleep'


if __name__ == '__main__':
    start_time = time.perf_counter()

    # processes = []
    # for _ in range(4):
    #     p = multiprocessing.Process(target=do_something, args=(1.5,))
    #     p.start()
    #     processes.append(p)
    # for process in processes:
    #     process.join()

    with concurrent.futures.ProcessPoolExecutor() as executor:
        futures = [executor.submit(do_something, 1) for _ in range(2)]

        for future in as_completed(futures):
            print(future.result())

    finish_time = time.perf_counter()

    print(f"Finished in {round(finish_time - start_time, 2)} second(s)")
```


欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。