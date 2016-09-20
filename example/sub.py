from websocket import create_connection
import time
import threading

ws = create_connection("ws://localhost:9900/ws")


def heartbeat():
    while True:
        ws.ping('x')
        time.sleep(30)

def recv():
    while True:
        result = ws.recv()
        print 'recv:', result



if __name__ == '__main__':
    threads = []
    t1 = threading.Thread(target=heartbeat, args=())
    t2 = threading.Thread(target=recv, args=())
    threads.append(t1)
    threads.append(t2)
    for t in threads:
        t.start()
