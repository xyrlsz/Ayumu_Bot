from Based.Event import Event
import requests
import json
from Based.Config import get_config
import asyncio

config = "Config/config.yaml"
get_config = get_config(config)


async def Remove_Msg(message_Event: Event):
    url = (
        "http://"
        + get_config["Host"]
        + "/v1/LuaApiCaller?funcname=MagicCgiCmd&timeout=10&qq="
        + get_config["QQBotUid"]
    )
    Uin = message_Event.getEventData().FromUin()
    MsgSeq = message_Event.getEventData().MsgSeq()
    MsgRandom = message_Event.getEventData().MsgRandom()
    payload = json.dumps(
        {
            "CgiCmd": "GroupRevokeMsg",
            "CgiRequest": {"Uin": Uin, "MsgSeq": MsgSeq, "MsgRandom": MsgRandom},
        }
    )
    headers = {
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


async def Ban_Member(GroupUin: int, SenderUid: str, BanTime: int = 60):
    url = (
        "http://"
        + get_config["Host"]
        + "/v1/LuaApiCaller?funcname=MagicCgiCmd&timeout=10&qq="
        + get_config["QQBotUid"]
    )

    payload = json.dumps(
        {
            "CgiCmd": "SsoGroup.Op",
            "CgiRequest": {
                "OpCode": 4691,
                "Uin": GroupUin,
                "Uid": SenderUid,
                "BanTime": BanTime,
            },
        }
    )
    headers = {
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


async def Remove_Member(GroupUin: int, SenderUid: str):
    url = (
        "http://"
        + get_config["Host"]
        + "/v1/LuaApiCaller?funcname=MagicCgiCmd&timeout=10&qq="
        + get_config["QQBotUid"]
    )

    payload = json.dumps(
        {
            "CgiCmd": "SsoGroup.Op",
            "CgiRequest": {
                "OpCode": 2208,
                "Uin": GroupUin,
                "Uid": SenderUid,
            },
        }
    )
    headers = {
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


async def Exit_Group(GroupUin: int):
    url = (
        "http://"
        + get_config["Host"]
        + "/v1/LuaApiCaller?funcname=MagicCgiCmd&timeout=10&qq="
        + get_config["QQBotUid"]
    )

    payload = json.dumps(
        {"CgiCmd": "SsoGroup.Op", "CgiRequest": {"OpCode": 4247, "Uin": GroupUin}}
    )
    headers = {
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Content-Type": "application/json",
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
