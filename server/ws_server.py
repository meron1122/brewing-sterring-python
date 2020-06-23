#!/usr/bin/python
import asyncio
import json
import websockets
from logic.kettle import Kettle

with open('appsettings.json') as f:
    settings = json.load(f)

kettle = Kettle(int(settings['kettle']['heater_pin']), int(settings['kettle']['paddle_pin']))


async def handler(websocket, path):
    while 1:
        try:
            message = json.loads(await websocket.recv())
            if message["command"] == "set_setpoint":
                kettle.set_setpoint(float(message["arg"]))
            if message["command"] == "set_paddle":
                kettle.set_paddle(bool(message["arg"]))
            if message["command"] == "emergency_stop":
                kettle.emergency_stop()

            status = json.dumps({"temperature": str(kettle.temp), "setpoint": str(kettle.get_setpoint()),
                                 "paddle": str(kettle.get_paddle())})
            await websocket.send(status)
            await asyncio.sleep(0.05)
        except websockets.ConnectionClosed:  # bad solution :<
            break

start_server = websockets.serve(handler, settings['websockets']['ip'], int(settings['websockets']['port']))
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()