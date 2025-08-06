from socket import *
from concurrent.futures import ProcessPoolExecutor as Pool
from threading import Thread

def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(15)
    with Pool(4) as pool:
        while True:
            client, addr = sock.accept()
            print("client is connected")
            Thread(target=fib_handler, args=(client,pool), daemon=True).start()

def fib(n):
    if n<=2:
        return 1
    return fib(n-1) + fib(n-2)
        
def fib_handler(client, pool):
    with client:
        while True:
            req = client.recv(100).decode('ascii')
            if req == "\n":
                break
            n = int(req)
            future = pool.submit(fib, n)
            result = future.result()
            # result = fib(n)
            resp = str(result) + "\n"
            resp_bytes = resp.encode('ascii')
            client.send(resp_bytes)
        print(f"${client} got closed")

if __name__ == '__main__':
    fib_server(('',27000))

# fib_server(('',27000))
