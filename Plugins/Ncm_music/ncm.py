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


async def send_song(message: Event):
    receiver = message.getEventData().SenderUin()
    if message.getEventData().FromUin() is not None:
        content = message.getEventData().Content()
        if content:
            song_name = content[content.find("点歌") + len("点歌") :]
            if content.find("点歌") > -1 and song_name.strip():
                try:
                    id = search_music_result(song_name)[0]["id"]
                    print()
                    # card = NcmCard(get_song_info(id)).card
                    song_url = "https://music.163.com/#/song?id=" + str(id)
                    print()
                    if message.getEventData().FromType() != 2:
                        send_message(
                            TextMessage(
                                receiver,
                                message.getEventData().FromType(),
                                "网易云音乐链接：" + song_url,
                            ),
                        )
                    else:
                        new_dict_array = [
                            {
                                "Nick": message.getEventData().SenderNick(),
                                "Uin": message.getEventData().SenderUin(),
                            },
                        ]

                        send_message(
                            TextMessage(
                                message.getEventData().FromUin(),
                                message.getEventData().FromType(),
                                "网易云音乐链接：" + song_url,
                                AtUinLists=new_dict_array,
                            ),
                        )

                except:
                    send_message(
                        TextMessage(
                            receiver,
                            message.getEventData().FromType(),
                            "获取链接失败",
                        ),
                    )
                return True
    return False
