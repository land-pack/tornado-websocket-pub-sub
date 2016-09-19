from websocket import create_connection
import time
import threading
import signal

ws = create_connection("ws://localhost:9909/ws")


def heartbeat():
    while True:
        ws.ping('x')
        time.sleep(3)

def recv():
    while True:
        print "Wait Reciving ..."                       #while True:
        result = ws.recv()
        print 'recv:', result

def subscriber(a, b):
    sub=raw_input("Please input your interest match name")
    ws.send('sub#%s' % sub)


signal.signal(signal.SIGINT, subscriber)

if __name__ == '__main__':
    
    threads = []
    t1 = threading.Thread(target=heartbeat, args=())
    t2 = threading.Thread(target=recv, args=())
    threads.append(t1)
    threads.append(t2)
    for t in threads:
        #t.setDaemon(True)
        t.start()
