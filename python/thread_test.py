#!/usr/bin/python

import threading, time
from threading import Thread

class Worker(Thread):
    def __init__(self, i, condition, workItems):
        threading.Thread.__init__(self)
        self.condition = condition
        self.workItems = workItems
        self.name = "worker %s" % i

    def run(self):
        # pattern of running thread:
        # acquire/while true/wait/notifyAll/release 
        print "Run worker %s" % self.name
        self.condition.acquire()
        while True:
            print "Waiting"
            self.condition.wait()
            self.condition.notifyAll()
            self.condition.release()
            break
        print "%s start working\n" % self.name
        for w in self.workItems:
            print w, ","

def runTest():
    condition = threading.Condition()
    threads = []
    i = 10
    for x in range(0, 3):
        items = [ n for n in range(i, i + 10) ]
        worker = Worker(x, condition, items)
        threads.append(worker)
        print items
        i += 10

    for w in threads:
        w.start()
        
    print "Sleep..."
    time.sleep(5)
    print "Start"
    # pattern of main controll
    condition.acquire()    
    condition.notifyAll()
    condition.release()


runTest()
