import asyncio
import json
import random
import websockets

from Based.Event import Event
from Based.Config import get_config

config = "Config/config.yaml"
config_data = get_config(config)  # Renamed the variable to avoid conflict
Host = config_data["Host"]
QQBotUid = config_data["QQBotUid"]
devicename = config_data["devicename"]
Myjson = config_data["json"]


# websocket client
SERCIVE_HOST = "127.0.0.1:8086"


async def Wsdemo():
    uri = "ws://{}/ws".format(SERCIVE_HOST)
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                greeting = await websocket.recv()
                EventJson = json.loads(greeting)
                EventName = EventJson["CurrentPacket"]["EventName"]
                EventData = EventJson["CurrentPacket"]["EventData"]

                print(f"<{EventData}\n")
                if Event(EventJson).getEventData().Content() is not None:
                    print(Event(EventJson).getEventData().Content() + "\n")
                    print(Event(EventJson).getEventData().FromUin())

    except Exception as e:
        # 断线重连
        t = random.randint(5, 8)
        print(f"< 超时重连中... { t}", e)
        await asyncio.sleep(t)
        await Wsdemo()


asyncio.get_event_loop().run_until_complete(Wsdemo())
