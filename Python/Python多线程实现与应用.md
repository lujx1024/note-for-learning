---
title: Python多线程实现与应用
tags: Python,多线程
renderNumberedHeading: true
grammar_cjkRuby: true
---
[TOC]

# 前言
- 进程：是程序，资源集合，进程控制块组成，是最小的资源单位
	特点：就对Python而言，可以实现真正的并行效果
	缺点：进程切换很容易消耗cpu资源，进程之间的通信相对线程来说比较麻烦　　
- 线程：是进程中最小的执行单位。
	特点无法利用多核，无法实现真正意义上的并行效果。
	优点：对于IO密集型的操作可以很好利用IO阻塞的时间


# 多线程的使用限制

对于`计算密集型`的python多线程来说，无法利用到多线程带来的效果， 在2.7时计算密集型的python多线程执行效率比顺序执行的效率还低的多，在python3.5中对这种情况进行了优化，基本能实现这种多线程执行时间和顺序执行时间差不多的效果。

对于`I/O密集型`的python多线程来说，GIL的影响不是很大，因为I/O密集型的python多线程进程，每个线程在等待I/O的时候，将会释放GIL资源，供别的线程来抢占。所以对于I/O密集型的python多线程进程来说，还是能比顺序执行的效率要高的
  
  
  # Python 多线程实现
  
  ## 直接使用`threading`模块
  
  ```
import time
import threading

start_time = time.perf_counter()

def do_something(seconds: int):
    """
    线程执行函数，使用sleep函数模拟耗时操作
    Args:
        seconds (int): 睡眠时间代表耗时操作

    """
    print(f"Sleep {seconds} second(s)...")
    time.sleep(seconds)
    return 'Done Sleeping'

# 创建线程对象，args以元组形式传递target函数的参数
thread_1 = threading.Thread(target=do_something, args=(1,))
# 线程启动
thread_1.start()

finish_time = time.perf_counter()
print(f"Finished in {round(finish_time - start_time, 2)} seconds...")
  ```
  
  ## 封装继承  
  
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

def do_something(seconds: int):
    """
    线程执行函数，使用sleep函数模拟耗时操作
    Args:
        seconds (int): 睡眠时间代表耗时操作

    """
    print(f"Sleep {seconds} second(s)...")
    time.sleep(seconds)
    return 'Done Sleeping'


thread_1 = MyThread(do_something, args=(2,))
thread_1.start()
  ```
  
  ## 线程阻塞
  使用`join`函数可使主线程阻塞，等待子线程完成后继续执行后续代码，多个线程同时阻塞的情况下，等待时间以最长子线程执行时间为准。以`threading`模块使用为例：

```
import time
import threading

start_time = time.perf_counter()

def do_something(seconds: int):
    """
    线程执行函数，使用sleep函数模拟耗时操作
    Args:
        seconds (int): 睡眠时间代表耗时操作

    """
    print(f"Sleep {seconds} second(s)...")
    time.sleep(seconds)
    return 'Done Sleeping'

# 创建线程对象，args以元组形式传递target函数的参数
thread_1 = threading.Thread(target=do_something, args=(1,))
thread_1 = threading.Thread(target=do_something, args=(2,))
# 线程启动
thread_1.start()
thread_2.start()

# 线程阻塞
thread_1.join()
thread_2.join()

finish_time = time.perf_counter()
print(f"Finished in {round(finish_time - start_time, 2)} seconds...")

```
主线程执行时间约为`3s`,由于`thread_1`执行时间约为`1s`,`thread_2`线程执行时间约为`3s`，故主线程的等候时间取最长子线程执行时间，约为`3s`.

## 多个线程的阻塞设置

在循环创建了多个线程时，对创建的线程列表中的成员进行全员`join`操作，需要注意，不能在创建线程的循环体内进行，需先创建全部的线程后，执行`join`操作。以上述执行方法为例：
```
# 错误方法

for _ in range(10):
	t = threading.Thread(target=do_something,args=(1,))
	t.start()
	t.join()
	
# 正确方法

thread_list = []
for _ in range(10):
	t = threading.Thread(target=do_something.args=(1,))
	t.start()
	thread_list.append(t)

for thread in thread_list:
	thread.join

```
上述代码中，错误方法所演示的代码。本质上是，在循环体中，创建一个线程，启动线程，等待线程执行完成后，在创建新的线程并执行，如此往复。

# 使用线程池`ThreadPoolExecutor`

线程池在系统启动时即创建大量空闲的线程，程序只要将一个函数提交给线程池，线程池就会启动一个空闲的线程来执行它。当该函数执行结束后，该线程并不会死亡，而是再次返回到线程池中变成空闲状态，等待执行下一个函数。
　　此外，使用线程池可以有效地控制系统中并发线程的数量。当系统中包含有大量的并发线程时，会导致系统性能急剧下降，甚至导致 Python 解释器崩溃，而线程池的最大线程数参数可以控制系统中并发线程的数量不超过此数。
  
  ## 相关API接口
  
   [官网](https://docs.python.org/dev/library/concurrent.futures.html)
 `concurrent.futures`模块提供了高度封装的异步调用接口，异步执行可以使用线程`ThreadPoolExecutor`执行，也可以使用`ProcessPoolExecutor`单独的进程执行。两者都实现了由抽象`Executor`类定义的相同接口。

  ```
ThreadPoolExecutor：线程池，提供异步调用

1、submit(fn, *args, **kwargs)
异步提交任务

2、map(func, *iterables, timeout=None, chunksize=1) 
取代for循环submit的操作

3、shutdown(wait=True) 
相当于进程池的pool.close()+pool.join()操作
wait=True，等待池内所有任务执行完毕回收完资源后才继续
wait=False，立即返回，并不会等待池内的任务执行完毕
但不管wait参数为何值，整个程序都会等到所有任务执行完毕
submit和map必须在shutdown之前

4、result(timeout=None)
取得结果

5、add_done_callback(fn)
回调函数
  ```
  ## 线程池的使用
  
  ### `submit()`的使用
  调用`submit()`方法，传入线程执行方法(本实例中，方法为`do_something`)，和执行方法需要的参数，多个参数使用列表或元组形式传入。返回`Future`对象，`Future`对象表示的是异步运算的执行结果
  
  ```import time
from concurrent.futures.thread import ThreadPoolExecutor

start_time = time.perf_counter()


def do_something(seconds: int):
    """
    线程执行函数，使用sleep函数模拟耗时操作
    Args:
        seconds (int): 睡眠时间代表耗时操作
    """
    print(f"Sleep {seconds} second(s)...")
    time.sleep(seconds)
    return 'Done Sleeping'

# 创建线程池对象
executor = ThreadPoolExecutor(max_workers=3)
# 创建线程执行对象
future = executor.submit(do_something, 3)
# 获取线程执行结果(阻塞式)
print(future.result())
finish_time = time.perf_counter()

print(f"Finished in {round(finish_time - start_time, 2)} seconds...")
```

### `map()`的使用

`Executor.map()`使用方法，基本与python内置map()方法类似，将参数中的`*iterable`对象成员依次传入参数fn中执行，返回由每个执行结果组成的列表。

```import time
from concurrent.futures.thread import ThreadPoolExecutor

start_time = time.perf_counter()


def do_something(seconds: int):
    """
    线程执行函数，使用sleep函数模拟耗时操作
    Args:
        seconds (int): 睡眠时间代表耗时操作
    """
    print(f"Sleep {seconds} second(s)...")
    time.sleep(seconds)
    return 'Done Sleeping'


# 创建线程池对象
executor = ThreadPoolExecutor(max_workers=3)
# 创建休眠时间列表
secs = [5, 4, 3, 2, 1]

# 依次从休眠时间列表中传入不同的休眠时间创建线程，并执行
results = executor.map(do_something, secs)
for result in results:
    print(result)

finish_time = time.perf_counter()
print(f"Finished in {round(finish_time - start_time, 2)} seconds...")
```

### 异步回调函数的使用

```
import time
from concurrent.futures._base import Future
from concurrent.futures.thread import ThreadPoolExecutor

start_time = time.perf_counter()


def do_something(seconds: int):
    """
    线程执行函数，使用sleep函数模拟耗时操作
    Args:
        seconds (int): 睡眠时间代表耗时操作
    """
    print(f"Sleep {seconds} second(s)...")
    time.sleep(seconds)
    return 'Done Sleeping'


def callback_method(future: Future):
    result = future.result()
    print(result)


# 创建线程池对象
executor = ThreadPoolExecutor(max_workers=3)
# 使用异步方法，回调
executor.submit(do_something, 3).add_done_callback(callback_method)

finish_time = time.perf_counter()
print(f"Finished in {round(finish_time - start_time, 2)} seconds...")
```
使用异步回调方法，主线程不再等待子线程执行结果而是继续执行，等待子线程执行结束后，调用回调方法，故上述示例的执行输出结果为：
```
Sleep 3 second(s)...
Finished in 0.0 seconds...
Done Sleeping
```

  
欢迎使用 **{小书匠}(xiaoshujiang)编辑器**，您可以通过 `小书匠主按钮>模板` 里的模板管理来改变新建文章的内容。