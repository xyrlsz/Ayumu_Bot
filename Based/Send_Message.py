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

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
