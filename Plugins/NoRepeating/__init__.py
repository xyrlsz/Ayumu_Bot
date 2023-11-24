LastMessage = {
    "Counts": 0,
    "Content": None,
}

from Based.Event import Event
from Based.Activity import Remove_Msg, Ban_Member
from Based.Send_Message import send_message
from Based.Message import TextMessage

MsgDataDict = {}


async def RemoveMsg(Message_Event: Event):
    now_msg = Message_Event.getEventData().Content()
    GroupUin = Message_Event.getEventData().FromUin()
    SenderUid = Message_Event.getEventData().SenderUid()
    # 初始化 MsgDataDict 中的 GroupUin
    if GroupUin not in MsgDataDict:
        MsgDataDict[GroupUin] = {"Counts": 1, "Content": now_msg}

    if now_msg:
        if now_msg == MsgDataDict[GroupUin]["Content"]:
            MsgDataDict[GroupUin]["Counts"] += 1
            if MsgDataDict[GroupUin]["Counts"] > 3:
                await Remove_Msg(Message_Event)
                await Ban_Member(GroupUin, SenderUid)
                send_message(TextMessage(GroupUin, 2, "打断施法！"))
        else:
            MsgDataDict[GroupUin]["Content"] = now_msg
            MsgDataDict[GroupUin]["Counts"] = 1
