import multiprocessing
import time

def spd(n,v):
    time.sleep(10)
    n.value = v*10


if __name__ == '__main__':
    v1 = 1
    num = multiprocessing.Value('d', 0)
    task = multiprocessing.Process(target=spd, args=(num,v1)) #,args=[0,200,180]
    task.start()
    task.join()
    print(num.value)
    while num.value == 0:
        time.sleep(0.1)
    #if task != None:
    time.sleep(1)
    print(num.value)
    print("done")