from gevent import pywsgi
from geventwebsocket.handler import WebSocketHandler
import gevent
from flask import Flask, jsonify, request
import json
import time
from threading import Thread

app = Flask(__name__)
# 日本語対応
app.config['JSON_AS_ASCII'] = False
# jsonをsortしない
app.config['JSON_SORT_KEYS'] = False
# 予約語
reserved_word = ['all', 'list', 'old_result_list']
# 最初からデータ入れておく場合
#result_list = {'foo1':'ほげええ',
#        'bar2':20180610}

result_list = {}
old_result_list = []
# REST用URL{{{
@app.route('/api/rest/v1/<keys>', methods=['GET', 'POST', 'DELETE'])
def api_rest(keys):
    global result_list
    # GET{{{
    if request.method == 'GET':
        if keys == 'all':
            result = { 'status':'OK', }
            result['result'] = result_list

        elif keys == 'list':
            result = { 'status':'OK', }
            result['result'] = list(result_list.keys())

        elif keys == 'old_result_list':
            result = { 'status':'OK', }
            result['result'] = old_result_list

        elif keys in result_list:
            result = { 'status':'OK', }
            result['result'] = result_list[keys]

        else:
            result = {
                    'status':'ERROR',
                    'message':'<' + keys + '>は存在しません'
                    }
    # GET}}}
    # POST{{{
    elif request.method == 'POST':
        if keys in reserved_word:
            result = {
                    'status':'ERROR',
                    'message':'<' + keys + '>は予約語です'
                    }
        else:
            result = {
                    'status':'OK',
                    }
            result_list[keys] = request.form
    # POST}}}
    # DELETE{{{
    elif request.method == 'DELETE':
        if keys in result_list:
            del result_list[keys]
            result = {
                    'status':'OK',
                    'message':'<' + keys + '>を削除しました'
                    }
        else:
            result = {
                    'status':'ERROR',
                    'message':'<' + keys + '>は存在しません'
                    }
    # DELETE}}}
    # 想定外{{{
    else:
        result = {
                'status':'ERROR',
                'message':'例外エラー'
                }
    # 想定外}}}
    print('REST access: {}, {}'.format(request.method, keys))
    print(result) # XXX:DEBUG
    return jsonify(result)
# REST用URL}}}
# WebSocket用URL{{{
@app.route('/api/ws/v1/<action>_<keys>')
def api_ws(action, keys):
    global result_list
    global old_result_list
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        idno = id(ws)
        # send{{{
        if action == 'send':
            while True:
                src = ws.receive()
                result_list[keys] = json.loads(src)
                print('WebSocket access: {}, {}'.format(action, keys))
                print(src) # XXX:DEBUG
        # send}}}
        # receive{{{
        elif action == 'receive':
            if keys in result_list:
                while True:
                    if keys in old_result_list:
                        if idno in old_result_list[keys]:
                            while True:
                                gevent.sleep(0) # XXX:threadさせるのに必要
                                if old_result_list[keys][idno] != result_list[keys]:
                                    break
                    result = {
                            'status':'OK',
                            }
                    result['result'] = result_list[keys]
                    try:
                        ws.send(json.dumps(result))
                    except:
                        print('WebSocket close: {}, {}'.format(action, keys))
                        if keys in old_result_list and idno in old_result_list[keys]:
                            del old_result_list[keys][idno]
                            if not old_result_list[keys]:
                                del old_result_list[keys]
#                            ws.close()
                            return 'ERROR' # XXX:何か返さないとエラーになる

                    print('WebSocket access: {}, {}'.format(action, keys))
                    print(result) # XXX:DEBUG
                    if keys in old_result_list:
                        old_result_list[keys].update({idno:result_list[keys]})
                    else:
                        old_result_list = {keys:{idno:result_list[keys]}}
            else:
                result = {
                        'status':'ERROR',
                        'message':'<' + keys + '>は存在しません'
                        }
                ws.send(json.dumps(result, ensure_ascii=False))
                print('WebSocket access: {}, {}'.format(action, keys))
                print(result) # XXX:DEBUG
        else:
            result = {
                    'status':'ERROR',
                    'message':'action<' + action + '>は存在しません'
                    }
            ws.send(json.dumps(result, ensure_ascii=False))
            print('WebSocket access: {}, {}'.format(action, keys))
            print(result) # XXX:DEBUG
        # receive}}}
    # websocket未使用{{{
    else:
        result = {
                'status':'ERROR',
                'message':'WebSocket API用のURLです'
                }
        print('REST access: {}, {}'.format(request.method, keys))
        print(result) # XXX:DEBUG
        return jsonify(result)
    # websocket未使用}}}
    return 'OK' # XXX:何か返さないとエラーになる
# WebSocket用URL}}}
def main():
    app.debug = True
# 外部から接続可能
#    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app, handler_class=WebSocketHandler)
# localeのみ
    server = pywsgi.WSGIServer(('127.0.0.1', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()

# vim: set foldmethod=marker:
