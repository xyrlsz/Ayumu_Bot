import json
import random

from Based.Config import QQBotUid
from Based.Event import Event
from Based.Message import TextMessage
from Based.Send_Message import send_message


def random_dict(my_dict: dict):
    shuffled_keys = list(my_dict.keys())
    random.shuffle(shuffled_keys)

    # 创建一个新的字典，使用打乱后的键
    shuffled_dict = {key: my_dict[key] for key in shuffled_keys}
    return shuffled_dict


def merge_dicts(dict1, dict2):
    merged_dict = dict1.copy()

    for key, value in dict2.items():
        if key in merged_dict:
            # merged_dict[key] = [merged_dict[key], value]
            # if not isinstance(merged_dict[key], list):

            # else: merged_dict[key] + [value]
            if isinstance(merged_dict[key], list):
                if isinstance(value, list):
                    merged_dict[key] = merged_dict[key] + value
                else:
                    merged_dict[key].append(value)
            else:
                if isinstance(value, list):
                    # merged_dict[key] = merged_dict[key] + value
                    merged_dict[key] = value.append(merged_dict[key])
                else:
                    # merged_dict[key].append(value)
                    merged_dict[key] = [merged_dict[key], value]

        else:
            merged_dict[key] = value

    return merged_dict


def get_anmime_text():
    with open("./data/anime.json", "r", encoding="utf-8") as file:
        # 读取并解析json数据
        data0 = json.load(file)
        # 打印数据类型和内容
        # print(type(data))
        # print(data)
    with open("./data/傲娇系二次元bot词库5千词V1.2.json", "r", encoding="utf-8") as file:
        # 读取并解析json数据
        data1 = json.load(file)
    with open("./data/可爱系二次元bot词库1.5万词V1.2.json", "r", encoding="utf-8") as file:
        # 读取并解析json数据
        data2 = json.load(file)

    tmp = merge_dicts(data0, data1)
    return merge_dicts(tmp, data2)


# animedata = random_dict(get_anmime_text())


# print(animedata)
def AnimeText(search_string: str) -> str:
    # 打开本地文件
    # global animedata
    animedata = random_dict(get_anmime_text())
    if search_string:
        # with open("./data/anime.json", "r", encoding="utf-8") as file:
        #     # 读取并解析json数据
        #     data0 = json.load(file)
        #     # 打印数据类型和内容
        #     # print(type(data))
        #     # print(data)
        # with open("./data/傲娇系二次元bot词库5千词V1.2.json", "r", encoding="utf-8") as file:
        #     # 读取并解析json数据
        #     data1 = json.load(file)
        # with open("./data/可爱系二次元bot词库1.5万词V1.2.json", "r", encoding="utf-8") as file:
        #     # 读取并解析json数据
        #     data2 = json.load(file)
        # data = [data0, data1, data2]
        # dictionary = data[random.randint(0, 2)]
        dictionary = animedata
        contains_key = any(key in search_string for key in dictionary.keys())
        # matching_key = next(
        #     (key for key in dictionary.keys() if key in search_string and key != ""), ""
        # )
        matching_key = next(
            (
                key
                for key in sorted(dictionary.keys(), key=len, reverse=True)
                if key in search_string and key != ""
            ),
            "",
        )

        if contains_key and matching_key is not None:
            list_length = len(dictionary[matching_key])
            random_number = random.randint(0, list_length - 1)
            res = dictionary[matching_key][random_number]
            return res
    return None


async def send_animetext(message: Event):
    if message.getEventData().isBot:
        return False
    if (
        message.getEventData().MsgBody()
        and message.getEventData().FromUin() != 856337734
    ):
        print(message.getEventData().MsgBody())
        receiver = message.getEventData().SenderUin()
        print(str(QQBotUid) + "->" + str(receiver))
        if message.getEventData().MsgBody() is not None:
            content = message.getEventData().Content()
            if content:
                last_index = content.rfind("真寻")

                ask = content[last_index + len("真寻") :]
                if message.getEventData().FromType() != 2 and last_index == -1:
                    ask = content
                if ask.strip():
                    mesg = AnimeText(ask)
                else:
                    mesg = "呼叫小真寻有什么事吗?"
                if mesg is not None:
                    # print(str(mesg))
                    if message.getEventData().FromType() != 2:
                        send_message(
                            TextMessage(
                                receiver,
                                message.getEventData().FromType(),
                                str(mesg),
                            ),
                        )
                    else:
                        new_dict_array = [
                            {
                                "Nick": message.getEventData().SenderNick(),
                                "Uin": message.getEventData().SenderUin(),
                            },
                        ]
                        if str(receiver) != str(QQBotUid) and content.rfind("真寻") > -1:
                            send_message(
                                TextMessage(
                                    message.getEventData().FromUin(),
                                    message.getEventData().FromType(),
                                    str(mesg),
                                    AtUinLists=new_dict_array,
                                )
                            )

                    return True
    return False
