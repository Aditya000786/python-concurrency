from collections import deque
    
tasks = deque([])
def countdown(n):
    while n:
        yield n
        n-=1
# c = countdown(5)
# for i in c:
#     print(f"i={i}")
    
tasks = deque([])

tasks.extend([countdown(10), countdown(5), countdown(20)])
print(tasks)

def run():
    while tasks:
        task = tasks.popleft()
        try:
            x = next(task)
            print(x)
            tasks.append(task)
        except StopIteration:
            print(f"end of task:{task}")

run()