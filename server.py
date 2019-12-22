#!/usr/bin/env python

import asyncio
import websockets
import json
import pathlib
import ssl

from user import User

rooms = {}

def create_user(websocket, name):
    return User(websocket, name)

async def create_room(websocket, payload):
    if payload["room_code"] in rooms.keys():
        await send_response(websocket, 400, "Room already exists")
    else:
        rooms[payload["room_code"]] = [websocket]
        await send_response(websocket, 200)

async def join_room(websocket, payload):
    if payload["room_code"] not in rooms.keys():
        await send_response(websocket, 404, "Room does not exist")
    else:
        rooms[payload["room_code"]].append(websocket)
        await send_response(websocket, 200)

async def leave_room(websocket, payload):
    room_code = payload["room_code"]

    if websocket in rooms[room_code]:
        rooms[room_code].remove(websocket)
        if len(rooms[room_code]) == 0:
            del rooms[room_code]
        await send_response(websocket, 200)
    else:
        await send_response(websocket, 404, "User was not found in room specified")

async def broadcast(websocket, payload):
    room_code = payload["room_code"]
    message_type = payload["message_type"]
    body = payload["body"]
    message = json.dumps({
        "message_type": message_type,
        "body": body
    })

    # TODO add check for image message type
    if message_type == "text":
        for socket in rooms[room_code]:
            await socket.send(message)

actions = {
    "create_room": create_room,
    "join_room": join_room,
    "leave_room": leave_room,
    "broadcast": broadcast
}

async def send_response(websocket, status, error_msg=None):
    msg_dict = {
        "status": status
    }
    if error_msg is not None:
        msg_dict["error_msg"] = error_msg

    json_msg = json.dumps(msg_dict)
    await websocket.send(json_msg)

async def server_loop(websocket, path):
    async for message in websocket:
        message = json.loads(message)
        if "action" not in message.keys():
            await send_response(websocket, 400, "No action provided")
        else:
            if message["action"] in actions.keys():
                await actions[message["action"]](websocket, message)

# TODO Handle exceptions for realsies
def exception_handler(loop, context):
    print('Exception handler called')

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
localhost_key = pathlib.Path(__file__).with_name("localhost.key")
ssl_context.load_cert_chain(localhost_pem, keyfile=localhost_key)
start_server = websockets.serve(server_loop, "localhost", 8765, ssl=ssl_context, ping_timeout=None)

asyncio.get_event_loop().set_exception_handler(exception_handler)
asyncio.get_event_loop().run_until_complete(start_server)
print("Server started")
asyncio.get_event_loop().run_forever()
