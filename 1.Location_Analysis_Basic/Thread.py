import threading
from time import ctime, sleep


def myFun1():
    for i in range(30):
        print("This is fun1 - {} - {}".format(i, ctime()))
        sleep(3)


def myFun3():
    for i in range(50):
        print("This is fun2 - {} - {}".format(i, ctime()))
        sleep(2)


threads = []
threads.append(threading.Thread(target=myFun1))
threads.append(threading.Thread(target=myFun3))

for t in threads:
    t.setDaemon(True)
    t.start()

print(type(t))

t.join()
