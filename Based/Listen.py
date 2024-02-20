import asyncio
import json
import random
import threading

import websockets

from Based.Config import config_data, Host, QQBotUid
from Based.Event import Event
from Based.Login import login_QQ
from Based.Stauts import get_Status
from Plugins import NoRepeating
from Plugins.Anime.Anime import send_animetext
from Plugins.Bili.BiliInfo import analysis_Bili
from Plugins.Ncm_music.ncm import send_song
from Plugins.NiGanMa import NiGanMa
from Plugins.SeTu import SeTu
from Plugins.SysInfo import getSysInfo, send_info
from Plugins.Daily_CheckIn import check_in


if get_Status(config_data):
    print("已登录")
else:
    print("未登录")
    login_QQ(config_data)

# websocket client
SERCIVE_HOST = Host

# 创建一个异步队列
queue = asyncio.Queue()

receive_forbidden_list = list(config_data["receive_forbidden"])

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
                    # if str(Message.getEventData().SenderUin()) != str(QQBotUid):
                    await queue.put(Message)
                else:
                    print("已过滤" + str(Message.getEventData().FromUin()) + "消息")

                del Message

    except Exception as e:
        # 断线重连
        t = random.randint(5, 8)
        print(f"< 超时重连中... {t}", e)
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

        tasks = [
            limited_task(sem, NoRepeating.RemoveMsg, message),
            limited_task(sem, analysis_Bili, message),
            limited_task(sem, send_song, message),
            limited_task(sem, SeTu, message),
            limited_task(sem, getSysInfo, message),
            limited_task(sem, NiGanMa, message),
        ]
        results = await asyncio.gather(*tasks)
        # print(results)

        if any(result is True for result in results):
            None
        else:
            await send_animetext(message)

        del message
        queue.task_done()


def run_asyncio_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(asyncio.gather(Wsdemo(), process_message()))


def run_threaded_tasks():
    loop = asyncio.new_event_loop()

    # 创建线程
    thread1 = threading.Thread(target=check_in, args=(797649367,))
    thread2 = threading.Thread(target=run_asyncio_loop, args=(loop,))

    # 开始线程
    thread1.start()
    thread2.start()

    # 等待线程结束
    thread1.join()
    thread2.join()


if __name__ == "__main__":
    run_threaded_tasks()
