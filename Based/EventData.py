import json


class EventData:
    def __init__(self, EventData: dict) -> None:
        self.__body = EventData

    def FromUin(self) -> int:
        return self.__body["MsgHead"]["FromUin"]

    def ToUin(self) -> int:
        return self.__body["MsgHead"]["ToUin"]

    def FromType(self) -> int:
        return self.__body["MsgHead"]["FromType"]

    def SenderUin(self):
        return self.__body["MsgHead"]["SenderUin"]

    def SenderNick(self) -> str:
        return self.__body["MsgHead"]["SenderNick"]

    def GroupCard(self) -> str:
        return self.__body["MsgHead"]["GroupInfo"]["GroupCard"]

    def GroupName(self) -> str:
        return self.__body["MsgHead"]["GroupInfo"]["GroupName"]

    def MsgBody(self) -> dict:
        if self.__body["MsgBody"] is not None:
            return dict(self.__body["MsgBody"])
        return None

    def Content(self) -> str:
        if self.MsgBody() is not None:
            return self.__body["MsgBody"]["Content"]
        return None
