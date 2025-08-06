import time
from socket import *

sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('', 26000))

while True:
    start = time.time()
    sock.send(b'33')
    resp = sock.recv(100)
    end = time.time()
    print(end-start)