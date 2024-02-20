from Based.EventData import EventData


class Event:
    def __init__(self, EventJson: dict):
        self.__body = EventJson

    def getName(self):
        return self.__body["CurrentPacket"]["EventName"]

    def getEventData(self):
        return EventData(self.__body["CurrentPacket"]["EventData"])
