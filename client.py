#!/usr/bin/env python

# WSS (WS over TLS) client example, with a self-signed certificate

import asyncio
import pathlib
import ssl
import websockets

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
localhost_pem = pathlib.Path(__file__).with_name("localhost.pem")
ssl_context.load_verify_locations(localhost_pem)



async def run():
    uri = "wss://localhost:8765"
    async with websockets.connect(
        uri, ssl=ssl_context, ping_timeout=None
    ) as websocket:
        while True:
            await websocket.send(input())

asyncio.get_event_loop().run_until_complete(run())
