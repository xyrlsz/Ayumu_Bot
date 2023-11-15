from bilireq import video
import json
import requests
import time
from datetime import datetime
import asyncio
import re
from typing import Union
import asyncio
import logging
import json
import random
from Based.Event import Event
from Based.Send_Message import send_message
from Plugins.Ncm_music.ncmcard import NcmCard
from Plugins.Ncm_music.ncm_info import search_music_result
from Plugins.Ncm_music.ncm_info import get_song_info
from Based.Message import CardMessage, TextWithImageMessage
from Based.Message import TextMessage
from Based.Config import get_config
import asyncio
from Based.ToUpload_File import UpFile

config = "Config/config.yaml"
config_data = get_config(config)  # Renamed the variable to avoid conflict
Host = config_data["Host"]
QQBotUid = config_data["QQBotUid"]
devicename = config_data["devicename"]
Myjson = config_data["json"]





def get_Pnum(url):
    # Define the regular expression pattern
    # pattern = r"\?p=(\d+)&"
    pattern = r"p=(\d+)&"
    # Use re.search to find the match
    match = re.search(pattern, url)

    # Check if a match is found
    if match:
        # Extract the number between ?p= and &
        extracted_number = match.group(1)
        return extracted_number
    else:
        return None


def get_Id(url):
    # Define the regular expression pattern
    pattern = r"/video/([^/]+)"

    # Use re.search to find the match
    match = re.search(pattern, url)

    # Check if a match is found
    if match:
        # Extract the characters after "/video/"
        extracted_chars = match.group(1)
        return extracted_chars

    return None


async def get_info(video_id: Union[int, str]):
    info = await video.get_video_base_info(video_id)
    return info


# info = asyncio.run(get_info())


def timestamp_to_date(timestamp, format="%Y-%m-%d %H:%M:%S") -> str:
    """
    将时间戳转换为格式化的日期字符串。

    参数:
    - timestamp: 待转换的时间戳（以秒为单位）。
    - format: 日期字符串的格式，默认为'%Y-%m-%d %H:%M:%S'。

    返回:
    格式化后的日期字符串。
    """
    date_time_object = datetime.fromtimestamp(timestamp)
    formatted_date = date_time_object.strftime(format)
    return formatted_date


def format_number(num) -> str:
    """
    将数字转换为以万为单位表示，保留一位小数。

    参数:
    - num: 待转换的数字。

    返回:
    以万为单位表示并保留一位小数的字符串。
    """
    if num < 10000:
        return str(num)
    else:
        num_in_wan = round(num / 10000, 1)
        return f"{num_in_wan} 万"


# # 打开文件，如果文件不存在则创建，如果存在则覆盖
# with open("output.txt", "w") as file:
#     # 将字符串写入文件
#     file.write(str(info))

# # 也可以使用相对或绝对路径
# # with open('/path/to/output.txt', 'w') as file:
# #     file.write('Hello, this is a string.')


class VideoInfo:
    def __init__(self, data: dict):
        self.__body = data
        self.__bvid = data.get("bvid")
        self.__aid = data.get("aid")
        self.__videos = data.get("videos")
        self.__tid = data.get("tid")
        self.__tname = data.get("tname")
        self.__copyright = data.get("copyright")
        self.__pic = data.get("pic")
        self.__title = data.get("title")
        self.__pubdate = data.get("pubdate")
        self.__desc = data.get("desc")
        self.__desc_v2 = data.get("desc_v2")[0]["raw_text"]
        self.__owner = data.get("owner")
        self.__dynamic = data.get("dynamic")
        self.__owner_name = data.get("owner")["name"]
        self.__cid = data.get("cid")
        self.__stat = data.get("stat")
        self.__pages = data.get("pages")

    def get_body(self):
        return self.__body

    def get(self, key: str):
        return self.__body["key"]

    def BVid(self):
        return self.__bvid

    def type_name(self):
        return self.__tname

    def aid(self):
        return self.__aid

    def Up_name(self):
        return self.__owner_name

    def Up_id(self):
        return self.__owner["mid"]

    def Up_face(self):
        return self.__owner["face"]

    def upload_time(self):
        return self.__pubdate

    def video_count(self):
        return self.__videos

    def video_name(self):
        return self.__title

    def video_desc(self):
        return self.__desc

    def video_desc_v2(self):
        return self.__desc_v2

    def video_pic(self):
        return self.__pic

    def video_tid(self):
        return self.__tid

    def video_dynamic(self):
        return self.__dynamic

    def video_view(self):
        return self.__stat["view"]

    def video_danmaku(self):
        return self.__stat["danmaku"]

    def video_reply(self):
        return self.__stat["reply"]

    def video_like(self):
        return self.__stat["like"]

    def video_coin(self):
        return self.__stat["coin"]

    def video_favorite(self):
        return self.__stat["favorite"]

    def video_share(self):
        return self.__stat["share"]

    def video_pages(self):
        return self.__pages

    def video_card(self, Pnum: str = None) -> str:
        video_info = self
        video_name = video_info.video_name()
        video_desc = video_info.video_desc()
        type_name = video_info.type_name()
        Up_name = video_info.Up_name()
        Upload_time = timestamp_to_date(video_info.upload_time())
        video_view = format_number(video_info.video_view())
        video_favorite = format_number(video_info.video_favorite())
        video_like = format_number(video_info.video_like())
        danmaku = format_number(video_info.video_danmaku())
        video_coin = format_number(video_info.video_coin())
        video_reply = format_number(video_info.video_reply())
        aid = video_info.aid()
        if Pnum:
            url = f"https://www.bilibili.com/video/av{aid}" + "/?p={}".format(Pnum)
            little_title = video_info.video_pages()[int(Pnum) - 1]["part"]
            mesg = f"""链接：{url}
标题：{video_name}
小标题：{little_title}
类型：{type_name} | UP主：{Up_name} | 日期：{Upload_time} 
播放：{video_view} | 弹幕：{danmaku} | 收藏：{video_favorite} 
点赞：{video_like} | 硬币：{video_coin} | 评论：{video_reply} 
简介：{video_desc} 
        """
        else:
            url = f"https://www.bilibili.com/video/av{aid}/"
            mesg = f"""
链接：{url}
标题：{video_name}
类型：{type_name} | UP主：{Up_name} | 日期：{Upload_time} 
播放：{video_view} | 弹幕：{danmaku} | 收藏：{video_favorite} 
点赞：{video_like} | 硬币：{video_coin} | 评论：{video_reply} 
简介：{video_desc} 
        """

        return mesg.strip()


logging.basicConfig(level=logging.INFO)


def extract_b23_tv_string(url):
    # 使用正则表达式提取目标字符串
    if url is None:
        return None
    pattern = r"b23\.tv/([^\s/?]+)"
    match = re.search(pattern, url)

    if match:
        return "https://" + str(match.group(0))
    else:
        return None


def get_short_url_idAndPnum(url: str):
    headers2 = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
    }

    # 示例使用 Chrome 91 版本的 User-Agent，你可以根据需要更新其中的版本号和其他信息。
    if url is None:
        return None
    response = requests.request("POST", url, headers=headers2)
    # print(response.text)
    return [get_Id(str(response.text)), get_Pnum(str(response.text))]


async def get_video_pic(url: str):
    videoId = get_Id(url)
    video_P = get_Pnum(url)
    info = await get_info(videoId)
    video_info = VideoInfo(info)
    return video_info.video_pic()


async def get_video_info_card(url: str):
    videoId = get_Id(url)
    video_P = get_Pnum(url)
    info = await get_info(videoId)
    video_info = VideoInfo(info)
    return video_info.video_card(video_P)

last_call_time = 0

def is_json(data):
    try:
        json.loads(data)
        return True
    except json.JSONDecodeError:
        return False

async def analysis_Bili(message: Event):
    global last_call_time
    # 获取当前时间戳
    current_time = time.time()
    if current_time - last_call_time < 10:
        return True
    Content = message.getEventData().Content()
    if is_json(str(Content)):
        parsed_data = json.loads(Content)
        Content = str(parsed_data)
    is_success = True

    if Content and (("bilibili.com/video" in Content) or ("b23.tv" in Content)):
        if Content.find("\/"):
            Content.replace("\/", "/")
            
        try:
            if "b23.tv" in Content:
                id_and_p = get_short_url_idAndPnum(extract_b23_tv_string(Content))
                if id_and_p[1] is None:
                    url_text = (
                        "https://www.bilibili.com/video/" + str(id_and_p[0]) + "/"
                    )
                else:
                    url_text = (
                        "https://www.bilibili.com/video/"
                        + str(id_and_p[0])
                        + "/?p="
                        + str(id_and_p[1])
                        + "/"
                    )

            else:
                url_text = Content
            print(url_text)
            card = await get_video_info_card(url_text)
            pic_url = await get_video_pic(url_text)
            receiver = message.getEventData().FromUin()
            Type = message.getEventData().FromType()
            logging.info(f"Card: {card}")
            logging.info(f"Pic URL: {pic_url}")
            pic = UpFile(Type, "FileUrl", pic_url)
            send_message(
                TextWithImageMessage(
                    receiver,
                    Type,
                    card,
                    pic.get_file_md5(),
                    pic.get_file_id()
                    # pic.get_height(),
                    # pic.get_width(),
                )
            )
            last_call_time = current_time
            return is_success
        except Exception as e:
            logging.error(f"Error in analysis_Bili: {e}")
            return False
