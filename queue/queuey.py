from collections import deque
from concurrent.futures import Future
from threading import Thread, Lock
from asyncio import wait_for, wrap_future, get_event_loop
from time import sleep
    
class Queuey:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.items = deque()
        self.getters = deque()
        self.putters = deque()
        self.mutex = Lock()
        
    def get_noblock(self):
        with self.mutex:
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
        with self.mutex:
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
        
    
    async def get_async(self):
        item, fut = self.get_noblock()
        if fut:
            item = await wait_for(wrap_future(fut), None)
        return item
    
    def put_sync(self, item):
        while True:
            fut = self.put_noblock(item)
            if fut is None:
                return
            fut.result()
            
    async def put_async(self, item):
        while True:
            fut = self.put_noblock(item)
            if fut is None:
                return
            await wait_for(wrap_future(fut), None)
            

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
        
async def aconsumer(q):
    while True:
        item = await q.get_async()
        if item is None:
            break
        print("Async Got: ", item)
        














