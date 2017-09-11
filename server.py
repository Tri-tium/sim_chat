from threading import Thread
from socket import socket

addr = ('0.0.0.0', 8080)

connections = {}

def notify(msg, exclude=None):
    me = connections[exclude]
    for ad, info in connections.items():
        if ad == exclude:
            continue
        author = me['name'] + ': '.encode()
        print(author, msg)
        info['con'].send(author + msg)

def handle(con, ad):
    connections[ad] = {
        'con': con,
        'name': str(ad).encode()
    }
    while True:
        data = con.recv(1024)
        if not data:
            del connections[ad]
            break
        if data.startswith('/name '.encode()):
            name = data[6:]
            connections[ad]['name'] = name
            continue

        print(data)
        t=Thread(target=notify, args=(data, ad))
        t.start()


with socket() as sock:
    sock.setsockopt(1, 2, 1)
    sock.bind(addr)
    sock.listen()
    while True:
        con, ad = sock.accept()
        t=Thread(target=handle, args=(con, ad))
        t.start()
