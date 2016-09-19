import redis
import time

r = redis.StrictRedis(host='127.0.0.1', port= 6379, db=1)

p =r.pubsub()
p.subscribe('first')


while True:
    message = p.listen()
    if message:
        print message
