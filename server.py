#!/usr/bin/env python

import asyncio
import websockets
import json
import pathlib
import ssl

from user import User

rooms = {}


async def create_room(websocket, payload):
    if payload["room_code"] in rooms.keys():
        await send_error(websocket, "Room already exists")
    else:
        user = User(websocket, )
        rooms[payload["room_code"]] = []

actions = {
    "create_room": create_room
}

async def send_error(websocket, error_msg):
    json_msg = json.dumps({
        "error": error_msg
    })
    await websocket.send(json_msg)

async def server_loop(websocket, path):
    while True:
        payload = json.loads(await websocket.recv())
        if "action" not in payload.keys():
            await send_error(websocket, "No action provided")
        else:
            if payload["action"] in actions.keys():
                await actions[payload["action"]](websocket, payload)

# TODO Handle exceptions for realsies
def exception_handler(loop, context):
    print('Exception handler called')

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
localhost_key = pathlib.Path(__file__).with_name("localhost.key")
ssl_context.load_cert_chain(localhost_pem, keyfile=localhost_key)
start_server = websockets.serve(server_loop, "localhost", 8765, ssl=ssl_context)

asyncio.get_event_loop().set_exception_handler(exception_handler)
asyncio.get_event_loop().run_until_complete(start_server)
print("Server started")
asyncio.get_event_loop().run_forever()
