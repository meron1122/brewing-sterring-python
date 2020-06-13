#!/usr/bin/python
import asyncio
import websockets
from logic.kettle import Kettle
import json

kettle = Kettle(23, 18)


async def handler(websocket, path):
    while 1:
        try:
            message = json.loads(await websocket.recv())
            if message["command"] == "get_status":
                status = json.dumps({"temperature": str(kettle.temp), "setpoint": str(kettle.get_setpoint()),
                                     "paddle": str(kettle.get_paddle())})
                await websocket.send(status)
            if message["command"] == "set_setpoint":
                kettle.set_setpoint(float(message["arg"]))
            if message["command"] == "set_paddle":
                kettle.set_paddle(bool(message["arg"]))

            await asyncio.sleep(0.5)
        except websockets.ConnectionClosed:  # bad solution :<
            break


start_server = websockets.serve(handler, "192.168.1.144", 8765)
print("test")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
