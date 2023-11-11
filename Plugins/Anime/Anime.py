import json
import random
from Based.Event import Event
from Based.Send_Message import send_message
from Plugins.Ncm_music.ncmcard import NcmCard
from Plugins.Ncm_music.ncm_info import search_music_result
from Plugins.Ncm_music.ncm_info import get_song_info
from Based.Message import CardMessage
from Based.Message import TextMessage
from Based.Config import get_config
import asyncio
config = "Config/config.yaml"
config_data = get_config(config)  # Renamed the variable to avoid conflict
Host = config_data["Host"]
QQBotUid = config_data["QQBotUid"]
devicename = config_data["devicename"]
Myjson = config_data["json"]


def AnimeText(search_string:str) -> str:
    # 打开本地文件
    if search_string:
        with open("./data/anime.json", "r", encoding="utf-8") as file:
            # 读取并解析json数据
            data = json.load(file)
            # 打印数据类型和内容
            # print(type(data))
            # print(data)

        dictionary = data
        contains_key = any(key in search_string for key in data.keys())
        matching_key = next((key for key in data.keys() if key in search_string), None)

        if contains_key and matching_key is not None:
            list_length = len(dictionary[matching_key])
            random_number = random.randint(0, list_length - 1)
            res = dictionary[matching_key][random_number]
            return res
    return None


async def send_animetext(message: Event):
    if message.getEventData().MsgBody() and message.getEventData().FromUin()!=856337734:
        print(message.getEventData().MsgBody())
        receiver = message.getEventData().SenderUin()
        print(str(QQBotUid)+"->"+str(receiver))
        if message.getEventData().MsgBody() is not None :
            content = message.getEventData().Content()
            if content :
                last_index = content.rfind("真寻")
                
                ask = content[last_index + len("真寻") :]
                if  message.getEventData().FromType() != 2 and last_index == -1:
                    ask = content
                if ask.strip() :
                    mesg = AnimeText(ask)
                else:

                    mesg = "呼叫小真寻有什么事吗?"
                if mesg is not None:
                    
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
                        if str(receiver) != str(QQBotUid) and content.rfind("真寻")>-1 :
                            send_message(
                                TextMessage(
                                    message.getEventData().FromUin(),
                                    message.getEventData().FromType(),
                                    mesg,
                                    AtUinLists=new_dict_array,
                                ),
                            )
            # if content and last_index != -1:
            #     ask = content[last_index + len("真寻"):]
            #     print()
            #     print(len(content))
            #     print(last_index)
            #     print(message.getEventData())
            #     if ask is not None:
            #         mesg = AnimeText(ask)
            #         if mesg is not None:
                        
            #             if message.getEventData().FromType() != 2:
            #                 send_message(
            #                     TextMessage(
            #                         receiver,
            #                         message.getEventData().FromType(),
            #                         mesg,
            #                     ),
            #                 )
            #             else:
            #                 new_dict_array = [
            #                     {
            #                         "Nick": message.getEventData().SenderNick(),
            #                         "Uin": message.getEventData().SenderUin(),
            #                     },
            #                 ]

            #                 send_message(
            #                     TextMessage(
            #                         message.getEventData().FromUin(),
            #                         message.getEventData().FromType(),
            #                         mesg,
            #                         AtUinLists=new_dict_array,
            #                     ),
            #                 )
            #     else :
            #         if message.getEventData().FromType() != 2:
            #             send_message(
            #                     TextMessage(
            #                         receiver,
            #                         message.getEventData().FromType(),
            #                         "呼叫小真寻有什么事吗？",
            #                     ),
            #             )
            #         else:
            #             new_dict_array = [
            #                 {
            #                     "Nick": message.getEventData().SenderNick(),
            #                     "Uin": message.getEventData().SenderUin(),
            #                 },
            #             ]

            #             send_message(
            #                 TextMessage(
            #                     message.getEventData().FromUin(),
            #                     message.getEventData().FromType(),
            #                     "呼叫小真寻有什么事吗？",
            #                     AtUinLists=new_dict_array,
            #                 ),
            #             )
