import requests
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
import requests
import websockets

from Based.Event import Event
from Based.Send_Message import send_message
from Plugins.Ncm_music.ncmcard import NcmCard
from Plugins.Ncm_music.ncm_info import search_music_result
from Plugins.Ncm_music.ncm_info import get_song_info
from Based.Message import CardMessage
from Based.Message import TextMessage
from Plugins.Ncm_music.ncm import send_song
from Plugins.Anime.Anime import send_animetext

import requests
import base64
from PIL import Image
from io import BytesIO
import requests
import json
from Based.Stauts import get_Status
from Based.Login import login_QQ
from Based.Config import get_config
from Based.Message import TextMessage
from Based.Message import ImageMessage
from Based.Message import VoiceMessage
from Based.Message import NormalMessage
from Based.Message import TextWithImageMessage
from Based.Message import CardMessage
from Based.Send_Message import send_message
from Based.ToUpload_File import UpFile

config = "Config/config.yaml"
get_config = get_config(config)

if get_Status(get_config):
    print("已登录")
else:
    print("未登录")
    login_QQ(get_config)


# websocket client
SERCIVE_HOST = "127.0.0.1:8086"

# 创建一个异步队列
queue = asyncio.Queue()


async def Wsdemo():
    uri = "ws://{}/ws".format(SERCIVE_HOST)
    try:
        async with websockets.connect(uri) as websocket:
            while True:
                greeting = await websocket.recv()
                EventJson = json.loads(greeting)
                EventName = EventJson["CurrentPacket"]["EventName"]
                EventData = EventJson["CurrentPacket"]["EventData"]
                Message = Event(EventJson)
                # 把Message对象放入队列
                await queue.put(Message)

    except Exception as e:
        # 断线重连
        t = random.randint(5, 8)
        print(f"< 超时重连中... { t}", e)
        await asyncio.sleep(t)
        await Wsdemo()


def Todo(message: Event):
    if message.getEventData().MsgBody() is not None:
        print(message.getEventData().MsgBody())


# def send_song(message: Event):
#     receiver = message.getEventData().SenderUin()
#     if message.getEventData().MsgBody() is not None:
#         content = message.getEventData().Content()
#         song_name = content[content.find("点歌") + len("点歌") :]
#         if content.find("点歌") > -1 and song_name.strip():
#             id = search_music_result(song_name)[0]["id"]
#             print()
#             # card = NcmCard(get_song_info(id)).card
#             song_url = "https://music.163.com/#/song?id=" + str(id)
#             print()
#             send_message(
#                 TextMessage(
#                     receiver, message.getEventData().FromType(), "网易云歌曲链接:\n" + song_url
#                 )
#             )


async def process_message():
    # 从队列里取出Message对象并处理
    while True:
        message = await queue.get()
        # do something with message
        # print(message.getEventData().Content())
        Todo(message)
        send_song(message)
        send_animetext(message)
        queue.task_done()


# 创建一个事件循环
loop = asyncio.get_event_loop()

# 把两个异步函数添加到事件循环
tasks = asyncio.gather(Wsdemo(), process_message())

# 运行
loop.run_until_complete(tasks)
