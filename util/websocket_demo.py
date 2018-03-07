# -*- coding: utf-8 -*-
import websocket
import time
import json
import requests



def on_open(ws):
    print('open', ws)
    # ws.send(json.dumps({'command': "ENTER_CHANNEL", 'data': {'chann_name': "live", 'cursor': '1885097'}}))
    arrOutput = { 0x14, 0x5F, 0x5F, 0x74, 0x69, 0x6D, 0x65, 0x01, 0x46, 0x7C, 0x49, 0x4E, 0x3B, 0x54, 0x49, 0x3D, 0x32, 0x30, 0x31, 0x38, 0x30, 0x32, 0x32, 0x38, 0x30, 0x36, 0x34, 0x34, 0x33, 0x30, 0x36, 0x35, 0x39, 0x3B, 0x55, 0x46, 0x3D, 0x35, 0x35, 0x3B, 0x7C };
    ws.send(arrOutput)


def on_close(ws):
    print('close')


def on_message(ws, message):
    print('message', message)


def on_error(ws, error):
    print(error)


def on_ping(ws, ping):
    print('ping', ping)


def on_pong(ws, pong):
    print('pong', pong)
    # ws.send('#' + "\u2219" + 'P' + "\u2219" + '__time,S_7324E9856EDB5E2D9A30045241348FB4000004' + "\u2219")


def on_content_message(ws, msg, flag):
    print('on_content_message', msg, flag)


def on_data(ws, data, type, flag):
    print('on_data', data, type, flag)


def create_client():
    url = 'wss://premws-pt3.365pushodds.com/zap/?uid=9266403232072562'
    headers = {
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh,zh-CN;q=0.9,en;q=0.8",
        "Cache-Control": "no-cache",
        "Connection": "Upgrade",
        "Host": "premws-pt13.365lpodds.com",
        'Origin': 'https://www.356884.com',
        "Pragma": "no-cache",
        "Sec-WebSocket-Extensions": "permessage-deflate; client_max_window_bits",
        "Sec-WebSocket-Key": "FUcG2ktlkM7SJJ4d75LSBA==",
        "Sec-WebSocket-Protocol": "zap-protocol-v1",
        "Sec-WebSocket-Version": "13",
        "Upgrade": "websocket",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    ws = websocket.WebSocketApp(url=url,
                                header=headers,
                                on_open=on_open,
                                on_close=on_close,
                                on_message=on_message,
                                on_error=on_error,
                                #on_ping=on_ping,
                                #on_cont_message=on_content_message,
                                #on_pong=on_pong,
                                #on_data=on_data,
                                keep_running=True)
    #ws.run_forever(ping_interval=2, host='premws-pt13.365lpodds.com', origin='https://www.356884.com')
    ws.run_forever()
    #ws.send({'command': "ENTER_CHANNEL", 'data': {'chann_name': "live", 'cursor': "1884716"}}, websocket.ABNF.OPCODE_MAP)


def create_hej():
    url = 'wss://realtime-prod.wallstreetcn.com/ws'
    headers = {
     'Accept-Encoding':'gzip, deflate, br',
    'Accept-Language':'zh,zh-CN;q=0.9,en;q=0.8',
    'Cache-Control':'no-cache',
    'Connection':'Upgrade',
    'Cookie':'wscnuid=CgQmYFpElPE8VwrnA94aAg==; _ga=GA1.2.601591017.1514445154; _gid=GA1.2.531869237.1519717799',
    'Host':'realtime-prod.wallstreetcn.com',
    'Origin':'https://wallstreetcn.com',
    'Pragma':'no-cache',
    'Sec-WebSocket-Extensions':'permessage-deflate; client_max_window_bits',
    'Sec-WebSocket-Key':'mNifRQ3cbNKIaJQN2cA7XQ==',
    'Sec-WebSocket-Version': '13',
    'Upgrade':'websocket',
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'
    }
    ws = websocket.WebSocketApp(url=url,
                                #header=headers,
                                on_open=on_open,
                                on_close=on_close,
                                on_message=on_message,
                                on_error=on_error,
                                #on_ping=on_ping,
                                #on_cont_message=on_content_message,
                                on_pong=on_pong,
                                #on_data=on_data,
                                keep_running=True)
    ws.run_forever()

if __name__ == '__main__':
    #rp = requests.post(url='https://premlp-pt3.365pushodds.com/pow2/', data='method=0&transporttimeout=20&type=F&topic=__time%2CS_FD6F82DA27C94AAEB73538555AE50730000003')
    data = 'method=0&transporttimeout=20&type=F&topic=__time%2CS_0D5105E30F3C4028824B10B6EBA66ED1000003'
    url1 = 'https://premlp-pt3.365pushodds.com/pow2/'
    url2 = 'https://pshudlp.365pushodds.com/pow2/'

    rp = requests.post(url=url1, data=data)
    id1 = rp.text[4:]
    print('id1', id1)

    rp = requests.post(url=url2, data=data)
    id2 = rp.text[4:]
    print('id2', id2)

    #rp = requests.post(url=url2+'?id='+ id2, data='method=1&s=0&topic=&clientid=' + id2)
    print(rp.text)
    i = 0
    while True:
        rp = requests.post(url='https://premlp-pt3.365pushodds.com/pow2/?id=' + id, data='method=1&s=15&topic=&clientid=' + id)
        print(rp.status_code, str(rp.content, 'utf-8'))
        time.sleep(2)
        i = i+1
        # https://pshudlp.365pushodds.com/pow2/   method=0&transporttimeout=20&type=F&topic=__time%2CS_558D14666EC94543843808DE0FE2F156000003
        # https://pshudlp.365pushodds.com/pow2/?id=IRUD05-AOIlp0HVFH2/  method=1&s=0&topic=&clientid=IRUD05-AOIlp0HVFH2%2F
