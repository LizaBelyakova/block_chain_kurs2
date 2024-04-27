import json
import sys
from fastapi import FastAPI
from typing import Any, Dict
from colorama import init
from colorama import Fore
import os
import requests

app = FastAPI()
init(autoreset=True)


@app.get('/', tags=['tech'])
def navigate_route():
    return {'Message': 'Hello, peer!'}


# send updates on this url
@app.post('/updates', tags=['tech'])
def updates(data: Dict[Any, Any]):
    print(Fore.GREEN + data['Message'].upper() + ':')
    if data['Message'] == 'Current BlockChain':
        blocks = json.loads(f"{data['data']}")
        [print(i) for i in blocks]
    elif data['Message'] == 'Peer connected':
        print(data['data'])
        print(Fore.GREEN + 'ALL PEERS IN NET:')
        curr_peers = requests.get('http://127.0.0.1:8000/peers').json()
        curr_peers.append(data['data'])
        [print(i) for i in curr_peers]
    elif data['Message'] == 'Peer left':
        print(data['data'])
        print(Fore.GREEN + 'ALL PEERS IN NET:')
        curr_peers = requests.get('http://127.0.0.1:8000/peers').json()
        [print(i) for i in curr_peers]
    else:
        print(data['data'])
    return data


@app.post('/mineBlock', tags=['blocks'])
def mine_block(data: str):
    try:
        requests.post(f'http://127.0.0.1:8000/mineBlock?data={data}')
    except:
        print("Connection failed")
    return


@app.get("/blocks", tags=['block'])
def blocks():
    try:
        return requests.get('http://127.0.0.1:8000/blocks').json()
    except:
        print("Connection failed. Main server probably not available")


if __name__ == '__main__':
    # 127.0.0.1, 8004 - for example
    host, port = sys.argv[1], sys.argv[2]
    print(Fore.MAGENTA + 'INFO:    ', 'Uvicorn running on',
          f'http://{host}:{port}',
          '(Press CTRL+C to quit)')
    print(Fore.LIGHTCYAN_EX + 'CURRENT BLOCKCHAIN:')
    try:
        [print(i) for i in requests.get('http://127.0.0.1:8000/blocks').json()]
        requests.post('http://127.0.0.1:8000/addPeer', json={'key': 'simple_key', 'peer_data': [host, port]})
    except:
        print("Connection failed. Main server probably not available")

    # running server through terminal : python clientServer.py 127.0.0.1 8003
    # --log-level critical - hide all uvicorn logs
    try:
        os.system(f'uvicorn clientServer:app --host {host} --port {port} --log-level critical')
    except KeyboardInterrupt:
        requests.post('http://127.0.0.1:8000/addPeer', json={'key': 'CLOSED', 'peer_data': [host, port]})
        print(Fore.RED + "INFO:     Finished server process [12440]")
        exit()

