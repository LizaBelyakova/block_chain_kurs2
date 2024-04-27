from fastapi import FastAPI
from block import BlockChain, generate_new_block
import uvicorn
import requests
from typing import Any, Dict, Optional


app = FastAPI()
MyBlockChain = BlockChain()

host, port = '127.0.0.1', 8000

peers_list = []


def send_updates(message: str, data: Optional[Any]):
    for i in peers_list:
        print(i[0], i[1])
        requests.post(f'http://{i[0]}:{i[1]}/updates', json={'Message': message, 'data': data})


@app.get('/', tags=['tech'])
def navigate_route():
    return {'Message': 'Welcome!'}


@app.get("/blocks", tags=['block'])
def blocks():
    return MyBlockChain.chain


@app.post("/mineBlock", tags=['block'])
def mine_block(data: str):
    new_block = generate_new_block(MyBlockChain, data)
    MyBlockChain.add_block(new_block)
    send_updates('Block added: ', str(repr(new_block)))
    send_updates('Current blockchain: ', str(MyBlockChain.chain))
    return MyBlockChain.chain


@app.get("/peers", tags=['peers'])
def peers():
    return peers_list


@app.post("/addPeer", tags=['peers'])
def add_peer(data: Dict[Any, Any]):
    if data['key'] == 'CLOSED' and data['peer_data'] in peers_list:
        peers_list.remove(data['peer_data'])
        send_updates("Peer left", data['peer_data'])
    if data['key'] != 'CLOSED':
        send_updates('Peer connected', data['peer_data'])
        peers_list.append(data['peer_data'])
    return peers_list


if __name__ == "__main__":
    uvicorn.run(app, host=host, port=port)

