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
