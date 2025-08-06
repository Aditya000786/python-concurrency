from socket import *
from threading import Thread
    
def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    while True:
        client, addr = sock.accept()
        print("client", client)
        print("addr", addr)
        Thread(target=fib_handler, args = (client,)).start()
        
        

def fib(num: int) -> int:
    if num<=2:
        return 1
    return fib(num-1) + fib(num-2)

def fib_handler(client):
    while True:
        req = client.recv(100).decode('ascii')
        if not req or req =='\n':
            break
        req = int(req)
        res = str(fib(req))
        resp = res.encode('ascii')+b'\n'
        client.send(resp)
    print("Closed for client", client)
    
fib_server(('', 26000))

