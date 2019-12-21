#!/usr/bin/env python

import asyncio
import websockets

async def connect(websocket):
    payload = await websocket.recv()
    print(payload)
    await websocket.send(payload)

routes = {
    "/connect": connect
}

async def router(websocket, path):
    await routes[path](websocket)

start_server = websockets.serve(router, "localhost", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
