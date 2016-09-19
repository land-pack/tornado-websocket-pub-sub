import ujson
import time
import random
from tornado.websocket import WebSocketHandler
import tornado.ioloop
import tornado.web
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop
from tornado.gen import coroutine, Task
from tornadoredis import Client

rds = Client()

class MyWebSocketHandler(WebSocketHandler):
	"""
	"""

	clients_set = set()


	@staticmethod
	def publish(message):
		for c in MyWebSocketHandler.clients_set:
			c.write_message(message)

	def prepare(self):
                print 'listen publish ...'
		self.listen_pub()

	def check_origin(self, origin):
		return True

	
	def open(self):
		print 'A client has connected ...'
		MyWebSocketHandler.publish('%s  has joined ' % str(id(self)))
		MyWebSocketHandler.clients_set.add(self)

	
	def on_message(self, msg):
		if msg == 'x':		# ping ...
			self.write_message('you said:%s' % msg)
		elif msg == 'pub':
                        start = time.time()
			self.publish(news[random.randint(0,4)])
                        stop = time.time()
                        print 'coast time ==>',stop - start
		else:
			MyWebSocketHandler.publish('user: %s said: %s ' % (str(id(self)),msg))
	
	def on_close(self):
		MyWebSocketHandler.clients_set.remove(self)
		MyWebSocketHandler.publish('%s has left ' % str(id(self)))

	
	def write_message(self, msg):
		if not self.stream.closed():
			super(MyWebSocketHandler, self).write_message(msg)
		else:
			self.on_connection_close()
        def on_pong(self, data):
            self.write_message(data)


        @coroutine
        def listen_pub(self):
            def handle(msg):
                print msg.body
                self.publish(str(msg.body))

            yield Task(rds.subscribe, channels='pub')
            rds.listen(handle)


def make_app():
    return tornado.web.Application([
		    (r'/ws',MyWebSocketHandler),
		    ],
		    debug=True)

if __name__ == '__main__':
	app = make_app()
	app.listen(9901)
        tornado.ioloop.IOLoop.current().start()
