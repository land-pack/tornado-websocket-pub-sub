import time
import redis

r = redis.StrictRedis(host="127.0.0.1", port= 6379, db=1)

i = 0

while True:
    i += 1
    r.publish("first", "the i is " + str(i))
    print ("The is is " + str(i))
    time.sleep(1)
