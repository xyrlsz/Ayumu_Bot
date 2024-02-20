from Based.Config import QQBotUid


class EventData:
    def __init__(self, EventData: dict) -> None:
        self.__body = EventData
        self.isBot = self.SenderUin == QQBotUid

    def FromUin(self) -> int:
        return self.__body["MsgHead"]["FromUin"]

    def FromUid(self) -> str:
        return self.__body["MsgHead"]["FromUid"]

    def ToUin(self) -> int:
        return self.__body["MsgHead"]["ToUin"]

    def ToUid(self) -> int:
        return self.__body["MsgHead"]["ToUid"]

    def FromType(self) -> int:
        return self.__body["MsgHead"]["FromType"]

    def SenderUin(self) -> int:
        return self.__body["MsgHead"]["SenderUin"]

    def SenderUid(self) -> str:
        return self.__body["MsgHead"]["SenderUid"]

    def SenderNick(self) -> str:
        return self.__body["MsgHead"]["SenderNick"]

    def MsgSeq(self) -> int:
        return self.__body["MsgHead"]["MsgSeq"]

    def MsgTime(self) -> int:
        return self.__body["MsgHead"]["MsgTime"]

    def MsgRandom(self) -> int:
        return self.__body["MsgHead"]["MsgRandom"]

    def MsgUid(self) -> int:
        return self.__body["MsgHead"]["MsgUid"]

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
