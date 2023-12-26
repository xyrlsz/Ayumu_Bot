from Based.Event import Event
from pixivpy3 import *
import json
import random
from Based.Event import Event
from Based.Send_Message import send_message
from Plugins.Ncm_music.ncmcard import NcmCard
from Plugins.Ncm_music.ncm_info import search_music_result
from Plugins.Ncm_music.ncm_info import get_song_info
from Based.Message import TextMessage, TextWithImageMessage, ImageMessage
from Based.Config import get_config
import asyncio
from Based.ToUpload_File import UpFile
import os
import sys
import re
from datetime import datetime
from pixivpy3 import AppPixivAPI, ByPassSniApi

sys.dont_write_bytecode = True
config = "Config/config.yaml"
config_data = get_config(config)  # Renamed the variable to avoid conflict
Host = config_data["Host"]
QQBotUid = config_data["QQBotUid"]
devicename = config_data["devicename"]
Myjson = config_data["json"]

# api = AppPixivAPI()
# api.download()
# api.auth(refresh_token="NkxyNwB5G6f5eHmVpNcQwaG-v7YFfUkb5QvMGaLMDSA")

_REFRESH_TOKEN = "NkxyNwB5G6f5eHmVpNcQwaG-v7YFfUkb5QvMGaLMDSA"


class Pixiv:
    def __init__(self, refresh_token: str):
        # self.api = AppPixivAPI()
        # self.api.auth(refresh_token=refresh_token)
        sni = False

        if not sni:
            self.api = AppPixivAPI()
        else:
            self.api = ByPassSniApi()  # Same as AppPixivAPI, but bypass the GFW
            self.api.require_appapi_hosts()

        self.api.auth(refresh_token=refresh_token)

    def download(self, url: str, directory: str = "Pixiv/", filename: str = "tmp.jpg"):
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.api.download(url, directory, fname=filename)

    def get_illust(self, illust_id):
        illust = self.api.illust(illust_id)
        return illust

    def get_illust_comments(self, illust_id):
        comments = self.api.illust_comments(illust_id)
        return comments

    def get_illust_related(self, illust_id):
        related = self.api.illust_related(illust_id)
        return related

    def get_illust_bookmarks_detail(self, illust_id):
        bookmarks_detail = self.api.illust_bookmarks_detail(illust_id)
        return bookmarks_detail

    def search_illust(self, query, offset=0, mode="partial"):
        search_result = self.api.search_illust(query, offset=offset, mode=mode)
        return search_result

    def get_illust_ranking(self, mode="day", date="2019-01-01"):
        ranking = self.api.illust_ranking(mode=mode, date=date)
        return ranking

    def get_user_detail(self, user_id):
        user_detail = self.api.user_detail(user_id)
        return user_detail

    def get_user_illusts(self, user_id, type="illust", offset=0):
        user_illusts = self.api.user_illusts(user_id, type=type, offset=offset)
        return user_illusts

    def get_user_bookmarks_illust(self, user_id, restrict="public", offset=0):
        user_bookmarks_illust = self.api.user_bookmarks_illust(
            user_id, restrict=restrict, offset=offset
        )
        return user_bookmarks_illust

    def get_user_following(self, user_id, restrict="public", offset=0):
        user_following = self.api.user_following(
            user_id, restrict=restrict, offset=offset
        )
        return user_following

    def get_user_followers(self, user_id, offset=0):
        user_followers = self.api.user_followers(user_id, offset=offset)
        return user_followers

    def get_illust_detail(self, illust_id):
        illust_detail = self.api.illust_detail(illust_id)
        return illust_detail

    def get_illust_comments(self, illust_id):
        illust_comments = self.api.illust_comments(illust_id)
        return illust_comments

    def get_illust_bookmarks_detail(self, illust_id):
        illust_bookmarks_detail = self.api.illust_bookmarks_detail(illust_id)
        return illust_bookmarks_detail

    def get_illust_related(self, illust_id):
        illust_related = self.api.illust_related(illust_id)
        return illust_related

    def get_illust_ranking(self, mode="daily", date="", offset=0):
        illust_ranking = self.api.illust_ranking(mode=mode, date=date, offset=offset)
        return illust_ranking

    def get_illust_new(self, restrict="public", offset=0):
        illust_new = self.api.illust_new(restrict=restrict, offset=offset)
        return illust_new

    def get_illust_popular(self, restrict="public", offset=0):
        illust_popular = self.api.illust_popular(restrict=restrict, offset=offset)
        return illust_popular

    def get_illust_follow(self, restrict="public", offset=0):
        illust_follow = self.api.illust_follow(restrict=restrict, offset=offset)
        return illust_follow

    def get_user_profile_public(self, user_id):
        user_profile_public = self.api.user_profile_public(user_id=user_id)
        return user_profile_public

    def get_user_profile_private(self, user_id):
        user_profile_private = self.api.user_profile_private(user_id=user_id)
        return user_profile_private

    def get_illust_url(self, illust_id: int, size: str = "large") -> str:
        return self.get_illust_detail(illust_id).illust.image_urls[size]


def contains_command(user_input: str, command_list: list):
    """
    判断用户输入是否包含给定命令列表中的任何一个命令。

    参数：
    - user_input: 用户输入的字符串
    - command_list: 包含可能命令的列表

    返回：
    - 如果用户输入中包含任何一个命令，返回 True；否则返回 False。
    """
    for cmd in command_list:
        if cmd in user_input:
            return True
    return False


pixiv = Pixiv(_REFRESH_TOKEN)


async def SeTu(message: Event):
    global pixiv
    if message.getEventData().MsgBody():
        content = message.getEventData().Content()
        if content:
            content = content.strip()
            pid_cmd = [
                "pid:",
                "pid搜索",
                "pid",
                "https://www.pixiv.net/artworks/",
            ]

            pid_search_start_index = -1

            for cmd in pid_cmd:
                if cmd in content:
                    pid_search_start_index = content.find(cmd)
                    pid_search_start_index += len(cmd)
                    break
            one_pic_cmd = ["来张色图", "来张涩图"]

            if pid_search_start_index != -1:
                # pid_search_start_index += len("pid搜索")
                # pid = int(content[pid_search_start_index:])
                # print(pixiv.get_illust_url(pid))
                # print(pixiv.get_illust_detail(pid).illust.title)
                # print(pixiv.get_illust_detail(pid).illust.tags)
                # print(pixiv.get_illust_detail(pid).illust.user.name)

                # pixiv_pic = UpFile(
                #     message.getEventData().FromUin(),
                #     "FileUrl",
                #     pixiv.get_illust_url(pid),
                # )
                try:
                    pid = int(content[pid_search_start_index:])
                    pic_url = pixiv.get_illust_url(pid)
                    title = pixiv.get_illust_detail(pid).illust.title
                    title = title.replace("/", "·")
                    tags_jsons = pixiv.get_illust_detail(pid).illust.tags
                    author_name = pixiv.get_illust_detail(pid).illust.user.name
                    tags = ""
                    file_type = None
                    if pixiv.get_illust_url(pid).find("jpg") != -1:
                        file_type = "jpg"
                    elif pixiv.get_illust_url(pid).find("png") != -1:
                        file_type = "png"
                    fileName_ = f"{author_name}_{title}_{pid}.{file_type}"
                    directory = "./Pixiv/img/"
                    if os.path.isfile(directory + fileName_) is False:
                        pixiv.download(pic_url, directory=directory, filename=fileName_)
                    pic_path = f"{directory}" + f"{fileName_}"
                    for i in tags_jsons:
                        tags += "#" + i.name + "\n"
                    InfoText = (
                        f"""标题：\n{title}\n\n作者:\n{author_name}\n\ntags:\n{tags}"""
                    )
                except Exception as e:
                    print(e)
                    return False

                # print(pic_path)
                pixiv_pic = UpFile(
                    message.getEventData().FromType(), "FilePath", pic_path
                )

                send_message(
                    TextWithImageMessage(
                        message.getEventData().FromUin(),
                        message.getEventData().FromType(),
                        InfoText,
                        pixiv_pic.get_file_md5(),
                        pixiv_pic.get_file_id(),
                        pixiv_pic.get_height(),
                        pixiv_pic.get_width(),
                        pixiv_pic.get_file_size(),
                    )
                )
                del pixiv_pic
                return True

    return False
