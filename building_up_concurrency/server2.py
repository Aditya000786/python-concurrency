from socket import *
from fib import fib
from threading import Thread
from concurrent.futures import ProcessPoolExecutor as Pool

def fib_server(address):
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sock.bind(address)
    sock.listen(5)
    print("Server listening on", address)
    
    # Create the pool inside the server function to avoid multiprocessing issues
    with Pool(4) as pool:
        while True:
            client, addr = sock.accept()
            print("Connection", addr)
            Thread(target=fib_handler, args=(client, pool), daemon=True).start()

def fib_handler(client, pool):
    with client:
        while True:
            try:
                req = client.recv(100)
                if not req:
                    break
                n = int(req.strip())
                future = pool.submit(fib, n)
                res = future.result()
                resp = str(res).encode('ascii') + b'\n'
                client.send(resp)
            except ValueError:
                client.send(b'Invalid input\n')
            except Exception as e:
                client.send(f'Error: {e}\n'.encode('ascii'))
                break
    print("Closed connection")

if __name__ == '__main__':
    fib_server(('', 25000))
