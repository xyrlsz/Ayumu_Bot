import json
import time
from typing import Union

import requests

from Based.Config import Host, QQBotUid, send_forbidden
from Based.Message import TextMessage, ImageMessage,TextWithImageMessage,VoiceMessage


def send_message(message: Union[TextMessage, ImageMessage,TextWithImageMessage,VoiceMessage]):
    if message.get_body()["CgiRequest"]["ToUin"] in send_forbidden:
        print("已禁止发送消息给" + str(message.get_body()["CgiRequest"]["ToUin"]))
        return
    url = "http://{}/v1/LuaApiCaller?funcname=MagicCgiCmd&timeout=10&qq={}".format(
        Host, QQBotUid
    )

    payload = json.dumps(message.get_body())

    headers = {
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Content-Type": "application/json",
    }
    while True:
        try:
            # 尝试执行的代码
            response = requests.request("POST", url, headers=headers, data=payload)
            print(str(message.get_body()) + "\n")
            pass
        except Exception as e:
            print(f"发生错误: {e}")
            print("10秒后重试...")
            time.sleep(10)
        else:
            # 如果没有错误，跳出循环
            break

    print(response.text)
