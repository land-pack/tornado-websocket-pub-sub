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



class MyWebSocketHandler(WebSocketHandler):
	"""
    clients_matchs = {
            'user1':['match1', 'match2', ..],
            'user2':['match2', 'match3', ..],
            'user3':['match5', 'match2', ..],
            'user4':['match1', 'match5', ..],
        }
        
	"""

	clients_set = set()
        clients_matchs = {}
        rds = Client()
        
        def __init__(self,*args, **kwargs):
            super(MyWebSocketHandler,self).__init__(*args, **kwargs)
            if len(MyWebSocketHandler.clients_set) == 0:
                self.listen_pub()



	@staticmethod
	def publish(message,match=''):
            if len(MyWebSocketHandler.clients_set) == 0:
                return 
	    for c in MyWebSocketHandler.clients_set:
                # If this user have subscribe the match!  
                user_id = str(id(c))
                user_match_subscribes = MyWebSocketHandler.clients_matchs.get(user_id,[])
                if match is None and user_match_subscribes is None:
                    print 'Unknow match or No Subscribe any match'
                else:
                    print '--->my sub',user_match_subscribes
                    print '--->current match ',match 
                    if match in user_match_subscribes:
                        print 'see me ,i will sendd'
                        c.write_message(message)

	def prepare(self):
		#self.listen_pub()
                pass

	def check_origin(self, origin):
		return True

	
	def open(self):

		print 'A client has connected ...'
		MyWebSocketHandler.publish('%s  has joined ' % str(id(self)))
		MyWebSocketHandler.clients_set.add(self)

	
	def on_message(self, msg):
		if msg == 'echo':
			self.write_message('you said:%s' % msg)
		elif msg.startswith('sub'):
                    # Example: "sub#123|456|789"
                    # Mean, this user havesubscribe 123,456,789
                    matchs = msg.split('#')[1]
                    # matchs is a string split by `|`
                    sub_matchs = matchs.split('|')
                    MyWebSocketHandler.clients_matchs[str(id(self))]=sub_matchs

                elif msg.startswith('check'):
                    print 'MyWebSocketHandler.clients_matchs',MyWebSocketHandler.clients_matchs
                    self.write_message('My Subscribe:%s' % MyWebSocketHandler.clients_matchs.get(str(id(self))))
		else:
			MyWebSocketHandler.publish('user: %s said: %s ' % (str(id(self)),msg))
	
	def on_close(self):
            if self in MyWebSocketHandler.clients_set:
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
                message = str(msg.body)
                print 'message', message
                if '|' in message:
                    news, match = message.split('|')

                    print 'news is ', news, 'match', match
                    self.publish(news, match)
            yield Task(self.rds.subscribe, channels='all')
            self.rds.listen(handle)
        



def make_app():
    return tornado.web.Application([
		    (r'/ws',MyWebSocketHandler),
		    ],
		    debug=True)

if __name__ == '__main__':
	app = make_app()
	app.listen(9909)
        tornado.ioloop.IOLoop.current().start()
