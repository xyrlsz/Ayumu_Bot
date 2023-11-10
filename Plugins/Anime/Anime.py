import json
import random
from Based.Event import Event
from Based.Send_Message import send_message
from Plugins.Ncm_music.ncmcard import NcmCard
from Plugins.Ncm_music.ncm_info import search_music_result
from Plugins.Ncm_music.ncm_info import get_song_info
from Based.Message import CardMessage
from Based.Message import TextMessage


def AnimeText(search_string) -> str:
    # 打开本地文件
    with open("./data/anime.json", "r", encoding="utf-8") as file:
        # 读取并解析json数据
        data = json.load(file)
        # 打印数据类型和内容
        # print(type(data))
        # print(data)

    dictionary = data
    contains_key = any(key in search_string for key in data.keys())
    matching_key = [key for key in data.keys() if key in search_string][0]
    if contains_key:
        list_length = len(dictionary[matching_key])
        random_number = random.randint(0, list_length - 1)
        res = dictionary[matching_key][random_number]
        return res
    return None


def send_animetext(message: Event):
    receiver = message.getEventData().SenderUin()
    if message.getEventData().FromUin() is not None:
        content = message.getEventData().Content()
        if content and content.find("真寻") != -1:
            mesg = AnimeText(content)
            if mesg is not None:
                print(message.getEventData())
                if message.getEventData().FromType() != 2:
                    send_message(
                        TextMessage(
                            receiver,
                            message.getEventData().FromType(),
                            mesg,
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
                            mesg,
                            AtUinLists=new_dict_array,
                        ),
                    )
