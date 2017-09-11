from socket import socket
from threading import Thread

addr = ('0.0.0.0', 8080)

def listen(server):
    while True:
        data = server.recv(1024)
        if not data:
            break
        print(data)


with socket() as sock:
    sock.connect(addr)
    t = Thread(target=listen, args=[sock])
    t.start()
    while True:
        s = input()
        sock.send(s.encode())
