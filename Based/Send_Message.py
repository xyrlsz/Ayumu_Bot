import time
import requests
import json

from Based.Config import get_config
from Based.ToUpload_File import UpFile

config = "Config/config.yaml"
get_config = get_config(config)

Host = get_config["Host"]
QQBotUid = get_config["QQBotUid"]
devicename = get_config["devicename"]
Myjson = get_config["json"]
send_forbidden = get_config["send_forbidden"]


def send_message(message):
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
            pass
        except Exception as e:
            print(f"发生错误: {e}")
            print("10秒后重试...")
            time.sleep(10)
        else:
            # 如果没有错误，跳出循环
            break

    print(response.text)
