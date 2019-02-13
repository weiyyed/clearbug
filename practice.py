import threading
import time

def long_time_task(i):
    print('当前子线程: {} - 任务{}'.format(threading.current_thread().name, i))
    time.sleep(3)
    print("结果: {}".format(8 ** 20))


if __name__=='__main__':
    start = time.time()
    print('这是主线程：{}'.format(threading.current_thread().name))
    t1 = threading.Thread(target=long_time_task, args=(1,),name='ww')
    t2 = threading.Thread(target=long_time_task, args=(2,),name='ww')
    t1.start()
    t2.start()
    for x in threading.enumerate():
        print("迭代",x)
        if 'ww' in x.getName():
            print(1110000)
    # print(threading.enumerate())
end = time.time()
print("总共用时{}秒".format((end - start)))
print(threading.enumerate())
