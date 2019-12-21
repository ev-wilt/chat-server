#!/usr/bin/env python

import asyncio
import websockets
import json

rooms = {}


async def create_room(websocket, payload):
    if payload["room_code"] in rooms.keys():
        await send_error(websocket, "Room already exists")
    else:
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

start_server = websockets.serve(server_loop, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
print("Server started")
asyncio.get_event_loop().run_forever()
