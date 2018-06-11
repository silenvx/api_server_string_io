import websocket
import time
from threading import Thread
import json

def on_message(ws, message):
    print('receive: {}'.format(json.loads(message)))


def main():
    ws = websocket.WebSocketApp('ws://127.0.0.1:5000/api/ws/v1/receive_date', on_message=on_message)
    ws.run_forever()

if __name__ == '__main__':
    main()
