from Based.Event import Event
from Based.Activity import Remove_Msg, Ban_Member
from Based.Send_Message import send_message
from Based.Message import TextMessage


LastMessage = {
    "Counts": 0,
    "Content": None,
}


MsgDataDict = {}

is_Interrupt = False


async def RemoveMsg(Message_Event: Event):
    now_msg = Message_Event.getEventData().Content()
    GroupUin = Message_Event.getEventData().FromUin()
    SenderUid = Message_Event.getEventData().SenderUid()
    global is_Interrupt
    # 初始化 MsgDataDict 中的 GroupUin
    if GroupUin not in MsgDataDict:
        MsgDataDict[GroupUin] = {"Counts": 1, "Content": now_msg}

    if now_msg:
        if now_msg == MsgDataDict[GroupUin]["Content"]:
            MsgDataDict[GroupUin]["Counts"] += 1

            if (
                MsgDataDict[GroupUin]["Counts"] > 3
                and Message_Event.getEventData().isBot == False
            ):
                # await Remove_Msg(Message_Event)
                # await Ban_Member(GroupUin, SenderUid)
                if is_Interrupt == False:
                    # send_message(TextMessage(GroupUin, 2, "打断施法！"))
                    if MsgDataDict[GroupUin]["Content"] != "打断施法！":
                        send_message(TextMessage(GroupUin, 2, "打断施法！"))
                        MsgDataDict[GroupUin]["Counts"] = 1
                        MsgDataDict[GroupUin]["Content"] = "打断施法！"
                    else:
                        None
                    await Remove_Msg(Message_Event)
                    await Ban_Member(GroupUin, SenderUid)
                    is_Interrupt = True
                else:
                    if MsgDataDict[GroupUin]["Content"] == "打断施法！":
                        await Remove_Msg(Message_Event)
                        await Ban_Member(GroupUin, SenderUid)
        else:
            MsgDataDict[GroupUin]["Content"] = now_msg
            MsgDataDict[GroupUin]["Counts"] = 1
            is_Interrupt = False
    else:
        MsgDataDict[GroupUin]["Counts"] = 0
        MsgDataDict[GroupUin]["Content"] = ""
        is_Interrupt = False

    return is_Interrupt
