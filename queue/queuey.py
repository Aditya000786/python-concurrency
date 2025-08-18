from collections import deque
from concurrent.futures import Future
from threading import Thread
class Queuey:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.items = deque()
        self.getters = deque()
        self.putters = deque()
        
    def get_noblock(self):
        if self.items:
            # Wake a putter
            if self.putters:
                self.putters.popleft().set_result(True)
            return self.items.popleft(), None
        else:
            fut = Future()
            self.getters.append(fut)
            return None, fut
            
    def put_noblock(self, item):
        if len(self.items) < self.maxsize:
            self.items.append(item)
            if self.getters:
                self.getters.popleft().set_result(
                    self.items.popleft()
                )
        else:
            fut = Future()
            self.putters.append(fut)
            return fut
        
    def get_sync(self):
        item, fut = self.get_noblock()
        if fut:
            item = fut.result()
        return item
        
    def put_sync(self, item):
        while True:
            fut = self.put_noblock(item)
            if fut is None:
                return
            fut.result()
            

def producer(q, n):
    for i in range(n):
        q.put_sync(i)
    q.put_sync(None)
    
def consumer(q, n):
    while True:
        item = q.get_sync()
        if item is None:
            break
        print("Got: ", item)