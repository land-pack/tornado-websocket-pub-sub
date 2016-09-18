# Tornado websocket  Pub/Sub

I have some news need to notify my clients, the simple ideas is :

```
for client in clients:
    client.send('some news ..')

```
The above code can be work fine, but if the client set have large ...
so the ideas is send the news with multi server

```
      A
     /
    /
Boss -----B-->
    \
     \
      C-->
      \
       -->
```     
