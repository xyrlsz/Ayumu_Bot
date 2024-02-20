# "https://git.acwing.com/HuParry/capoo/-/raw/master/capoo%20(10).gif?inline=false"

import random
import time
from Based.Event import Event
from Based.Message import ImageMessage
from Based.Send_Message import send_message
from Based.ToUpload_File import UpFile, img_url_to_based64


async def CapooPic(message: Event):
    try:
        base_url = "https://git.acwing.com/HuParry/capoo/-/raw/master/"

        if message.getEventData().isBot:
            return False
        content = message.getEventData().Content()
        if content == "capoo":
            random.seed(int(time.time()))
            random_num = random.randint(1, 456)
            url = base_url + f"capoo%20({random_num}).gif"
            file_base64 = img_url_to_based64(url)
            Type = message.getEventData().FromType()
            Capoo_Pic = UpFile(Type, "FileBase64", file_base64)

            send_message(
                ImageMessage(
                    message.getEventData().FromUin(),
                    Type,
                    Capoo_Pic.get_file_md5(),
                    Capoo_Pic.get_file_id(),
                    Capoo_Pic.get_height(),
                    Capoo_Pic.get_width(),
                    Capoo_Pic.get_file_size(),
                )
            )
            return True
    except Exception as e:
        print(e)
        return False
