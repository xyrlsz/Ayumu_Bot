# "https://git.acwing.com/HuParry/capoo/-/raw/master/capoo%20(10).gif?inline=false"

from asyncio import log
from io import BytesIO
import random
import time

from httpx import AsyncClient, ConnectError, ReadTimeout
from Based.Event import Event
from Based.Message import ImageMessage, TextMessage
from Based.Send_Message import send_message
from Based.ToUpload_File import UpFile, img_url_to_based64


async def LoongPic(message: Event):
    try:
        base_url = "https://git.acwing.com/Est/dragon/-/raw/main/"

        if message.getEventData().isBot:
            return False
        content = message.getEventData().Content()
        cmd = ["龙龙", "龙图"]
        if content in cmd:
            random.seed(int(time.time()))
            batch_choice = random.choice(["batch1/", "batch2/", "batch3/"])
            extensions = [".jpg", ".png", ".gif"]
            Type = message.getEventData().FromType()
            if batch_choice == "batch1/":
                selected_image_number = random.randint(1, 500)
            elif batch_choice == "batch2/":
                selected_image_number = random.randint(501, 1000)
            else:
                selected_image_number = random.randint(1001, 1516)

            for ext in extensions:
                image_url = (
                    f"{base_url}{batch_choice}dragon_{selected_image_number}_{ext}"
                )
                try:
                    async with AsyncClient() as client:
                        resp = await client.get(image_url, timeout=5.0)

                    if resp.status_code == 200:
                        file_base64 = img_url_to_based64(image_url)
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
                        # break

                # except FinishedException:
                #     raise

                except ConnectError:
                    log.error(f"连接错误：无法访问 {image_url}")
                    continue

                except ReadTimeout:
                    log.error(f"读取超时：{image_url}")
                    continue

                except Exception as e:
                    log.error(f"输出异常：{e}")
                    if ext == extensions[-1]:
                        await send_message(
                            TextMessage(
                                message.getEventData().FromUin(),
                                Type,
                                "龙龙现在出不来了，稍后再试试吧~",
                            )
                        )
                    return False
                    # break
    except Exception as e:
        log.error(f"输出异常：{e}")
        return False
