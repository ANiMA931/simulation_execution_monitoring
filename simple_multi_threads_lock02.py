import time
import threading

global num  # 在每个线程中都获取这个全局变量，每个线程都要用这个数据并可能对其修改
num = 100  # 设定一个共享变量的初值

def addNum(name, change_num, delay):
    global num  # 在每个线程中都获取这个全局变量，相当于拓扑矩阵M，每个线程都要用这个数据并可能对其修改
    lock.acquire()  # '''上锁
    temp = num
    time.sleep(0.0001)
    num = temp - change_num
    lock.release()  # '''释放这把锁，
    print("The current thread is " + name)  # 这一段不再需要上锁，因为这不是共同内容，这是各线程自己的事
    print("The current number is" + str(num))  # 这一段不再需要上锁，因为这不是共同内容，这是各线程自己的事
    time.sleep(delay)  # 这一段不再需要上锁，因为这不是共同内容，这是各线程自己的事



class MyThread(threading.Thread):  # 线程类继承式创建
    def __init__(self, name, change_num, delay):
        threading.Thread.__init__(self)
        self.name = name
        self.change_num = change_num
        self.delay = delay

    def run(self):  # 调用同一个函数，并赋予各自的实参
        addNum(self.name, self.change_num, self.delay)


if __name__ == '__main__':
    thread_list = []
    lock = threading.Lock()  # 创建一把锁
    for i in range(100):  # 创建100个线程，同时运行
        if (i % 2 == 0):
            a = 1
            b = 4
        else:
            a = 0
            b = 5  # 所有线程并发，系统总的耗时大体取决于delay最大者。

        t = MyThread(str(i), a, b)  # 创建线程,每个线程可以同时调用一个函数，并且向函数传递各自的实参
        t.start()  # 线程启动，随即运行run
        # print(threading.enumerate())  # 看一下当下的线程有哪些(观察后台的情况)
        thread_list.append(t)

    for t in thread_list:  # 主线程要等待所有线程执行完毕，方可结束
        t.join()

    print('Result: ', num)  # 由于仅偶数线程修改num值，故最终结果为50.
