# Tornado websocket  Pub/Sub

I have some news need to notify my clients, the simple ideas is :

```
for client in clients:
    client.send('some news ..')

```
The above code can be work fine, but if the client set have large ...
so the ideas is send the news with multi server

```
       /--->User1
      A --> User2
     /
    /
Boss -----B-->User3
    \
     \
      C-->User4
      \
       -->User5
``` 
The Boss want to say something, but don't need to call every user on the phone, just let his secretary know that.
so , we have some `tornado` run as different port, use `Nginx` as load balance server. see the code on `delegate.py`
And then to keep connection alive, we need to send heartbeat, so we have use multi-thread to do that. see the code on
`sub.py` we have a Boss, it's implementation just like the `sub.py` but don't need thread to send heartbeat, name as `pub.py`
to run all tornado instance with nginx, i have a configure file name as `websocket.conf` you just need to put on your nginx configure 
path and then restart your nginx will work! (my path is `/etc/nginx/conf.d/websocket.conf`) 

###Tornado & Redis
------
To manager your sub-publish, we have two way.

* 1 Message center send each sub-publish depend on different port!
* 2 Have broker to do sub/pub job between message center and sub-publish!

```
============================================================================

                                                                   ----user 1
                                                                  /----user 2
                                                      /---tornado A--->user 3
                                                     /-----tornado B
                                                    /-------tornado C
[[Message Center]] ---- publish a news --->> [Redis] ------------
                                                    \-------------
                                                     \--------------

{redis-cli}            { redis server }     { tornadoredis }  { websocket}
============================================================================
```

### How to run it ?
---

Simple, you can activate your env if you run on virtual env.
But don't forget install requirement before do that .
```
pip install -r requirements.txt
```
and then run your proxy server.

```
python proxy_server --port=9901
python proxy_server --port=9902
python proxy_server --port=9903
```
configuire your `websocket.conf` for your nginx and then restart your nginx.

```
cp websocket.conf /etc/nginx/conf.d/
```

And then run nginx as proxy load balance server.

```
service nginx restart
```
And then run a message center, just simultator a message publish center.

```
python new_center.py
```

Open a new terminal, play with the pub/sub server.

```
>>>from websocket import create_connection
>>>ws = create_connection('ws://localhost:9900/ws')
>>>ws.send('sub#77707|77708')
>>>ws.recv()
```
