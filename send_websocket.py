import websocket
import time
from threading import Thread
import datetime
import json

def get_date():
    result = {
            'date':datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            }
    return json.dumps(result, ensure_ascii=False)

def on_open(ws):
    def run():
        while True:
            message = get_date()
            print('send: {}'.format(message))
            ws.send(message)
            time.sleep(1)
    Thread(target=run).start()

def main():
    ws = websocket.WebSocketApp('ws://127.0.0.1:5000/api/ws/v1/send_date', on_open=on_open)
    ws.run_forever()

if __name__ == '__main__':
    main()
