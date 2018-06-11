api\_server\_string\_io
===
これは何か
---
python, flask, gevnet-websocketを利用して、REST API、もしくはWebSocket APIでJSONを送受信するAPI Serverです
REST API -> WebSocket APIや、その逆も保存名を同じにすればできます

使い方
---
サーバの起動
```
% python ./api_server.py
```

REST APIの送受信用URL
```
http://127.0.0.1:5000/api/rest/v1/<保存名>
```

WebSocket APIの送信用URL
```
http://127.0.0.1:5000/api/ws/v1/send_<保存名>
```

WebSocket APIの受信用URL
```
http://127.0.0.1:5000/api/ws/v1/receive_<保存名>
```


動作確認用プログラム
---
http postで保存名tickerにdate=2018/06/12, price=120000を保存
```
% curl -X POST 'http://127.0.0.1:5000/api/rest/v1/ticker' -d 'date=2018/06/12&price=120000'
{
  "status": "OK"
}
```
http getで保存名tickerを取得
```
% curl 'http://127.0.0.1:5000/api/rest/v1/ticker'
{
  "status": "OK",
  "result": {
    "date": "2018/06/12",
    "price": "120000"
  }
}

```

websocketで保存名dateに日時を送信
```
% python ./send_websocket.py
send: {"date": "2018/06/12 04:19:00"}
send: {"date": "2018/06/12 04:19:01"}
send: {"date": "2018/06/12 04:19:02"}
...
```
websocketで保存名dateを受信
```
% python ./receive_websocket.py
receive: {'status': 'OK', 'result': {'date': '2018/06/12 04:19:00'}}
receive: {'status': 'OK', 'result': {'date': '2018/06/12 04:19:01'}}
receive: {'status': 'OK', 'result': {'date': '2018/06/12 04:19:02'}}
...
```
