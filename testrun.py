__author__ = 'Yonatan'
import threading, time

def A(lock):

    while True:
        time.sleep(5)
        lock.acquire()
        print "Every 5"
        lock.release()

def B(lock):
    while True:
        time.sleep(5)
        lock.acquire()
        print "Every 1"
        lock.release()


lock = threading.Lock()
th1 = threading.Thread(target=A, args=(lock, ))
th2 = threading.Thread(target=B, args=(lock, ))
th1.start()
th2.start()
th1.join()
th2.join()

