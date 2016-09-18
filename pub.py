from websocket import create_connection
import threading

def send_news(port):
    ws = create_connection("ws://localhost:990%d/ws" % port )
    print "Sending 'Hello, World!' ..."
    ws.send("fresh")
    print "Sent"
    print "Reciving ..."
    result = ws.recv()
    print "Recived '%s'" % result
    ws.close()

if __name__ == '__main__':
    for i in xrange(3):
        i=i+1
        t = threading.Thread(target=send_news, args=(i,))
        t.start()

