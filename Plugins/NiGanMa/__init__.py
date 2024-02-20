from Based.Event import Event
from Based.Send_Message import send_message
from Based.ToUpload_File import UpFile
from Based.Message import VoiceMessage


async def NiGanMa(message: Event):
    if message.getEventData().isBot:
        return False
    try:
        content = message.getEventData().Content()
        if content:
            content = content.strip()
            if content == "你干嘛":
                cmd_id = 0
                if message.getEventData().FromType() == 1:
                    cmd_id = 26
                elif message.getEventData().FromType() == 2:
                    cmd_id = 29

                NiGanMaAudio = UpFile(cmd_id, "FilePath", "data/audio/niganma.amr")

                send_message(
                    VoiceMessage(
                        message.getEventData().FromUin(),
                        message.getEventData().FromType(),
                        NiGanMaAudio.get_file_md5(),
                        NiGanMaAudio.get_file_size(),
                        NiGanMaAudio.get_file_token(),
                    )
                )

                return True

    except Exception as e:
        print(e)

    return False
