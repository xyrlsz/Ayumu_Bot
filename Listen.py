import json
from Based.Config import get_config

config = "Config/config.yaml"
config_data = get_config(config)  # Renamed the variable to avoid conflict
Host = config_data["Host"]
QQBotUid = config_data["QQBotUid"]
devicename = config_data["devicename"]
Myjson = config_data["json"]

import asyncio
import json
import random

import websockets

from Based.Event import Event

from Plugins.Ncm_music.ncm import send_song
from Plugins.Anime.Anime import send_animetext


import json
from Based.Stauts import get_Status
from Based.Login import login_QQ
from Based.Config import get_config


from Plugins.Bili.BiliInfo import analysis_Bili
from Plugins import NoRepeating
from Plugins.SeTu import SeTu
from Plugins.SysInfo import getSysInfo, periodic_send_info

config = "Config/config.yaml"
get_config = get_config(config)

if get_Status(get_config):
    print("已登录")
else:
    print("未登录")
    login_QQ(get_config)


# websocket client
SERCIVE_HOST = Host

# 创建一个异步队列
queue = asyncio.Queue()

receive_forbidden_list = list(get_config["receive_forbidden"])

sem = asyncio.Semaphore(2)  # 限制同时运行的任务数量为2


async def Wsdemo():
    uri = "ws://{}/ws".format(SERCIVE_HOST)
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                greeting = await websocket.recv()
                EventJson = json.loads(greeting)
                # EventName = EventJson["CurrentPacket"]["EventName"]
                EventData = EventJson["CurrentPacket"]["EventData"]
                print(str(EventData) + "\n")
                Message = Event(EventJson)
                # 把Message对象放入队列
                if int(Message.getEventData().FromUin()) not in receive_forbidden_list:
                    if str(Message.getEventData().SenderUin()) != str(QQBotUid):
                        await queue.put(Message)
                else:
                    print("已过滤" + str(Message.getEventData().FromUin()) + "消息")

                del Message

    except Exception as e:
        # 断线重连
        t = random.randint(5, 8)
        print(f"< 超时重连中... { t}", e)
        await asyncio.sleep(t)
        await Wsdemo()


def Todo(message: Event):
    if message.getEventData().MsgBody() is not None:
        print(message.getEventData().MsgBody())


async def isCanSendAnimeText(message: Event):
    if await analysis_Bili(message) or send_song(message):
        None
    else:
        await send_animetext(message)


async def limited_task(sem, coro, message=None):
    async with sem:
        if message is not None:
            return await coro(message)
        else:
            return await coro


async def process_message():
    global sem
    while True:
        # 从队列里取出Message对象并处理
        message: Event = await queue.get()

        # do something with message
        # print(message.getEventData().Content())
        # Todo(message)

        # results = await asyncio.gather(
        # NoRepeating.RemoveMsg(message),
        # analysis_Bili(message),
        # send_song(message),
        # SeTu(message),
        # )
        # sem = asyncio.Semaphore(2)  # 限制同时运行的任务数量为2
        tasks = [
            limited_task(sem, NoRepeating.RemoveMsg, message),
            limited_task(sem, analysis_Bili, message),
            limited_task(sem, send_song, message),
            limited_task(sem, SeTu, message),
            limited_task(sem, getSysInfo, message),
        ]
        results = await asyncio.gather(*tasks)
        # print(results)

        if any(result is True for result in results):
            None
        else:
            await send_animetext(message)

        del message
        queue.task_done()


# 创建一个事件循环
loop = asyncio.get_event_loop()

# 把两个异步函数添加到事件循环
tasks = asyncio.gather(
    Wsdemo(),
    process_message(),
    limited_task(sem, periodic_send_info()),
)

# 运行
loop.run_until_complete(tasks)
