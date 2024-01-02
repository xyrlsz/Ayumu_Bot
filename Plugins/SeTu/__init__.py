import os
import random
import sys

import threading
import time

from pixivpy3 import AppPixivAPI, ByPassSniApi
from Based.Config import get_config
from Based.Event import Event
from Based.Message import TextWithImageMessage, TextMessage
from Based.Send_Message import send_message
from Based.ToUpload_File import UpFile

sys.dont_write_bytecode = True
config = "Config/config.yaml"
config_data = get_config(config)
Host = config_data["Host"]
QQBotUid = config_data["QQBotUid"]
devicename = config_data["devicename"]
Myjson = config_data["json"]

_REFRESH_TOKEN = "aLLNMJ4uFmqmj0seVbY62Xjv00Dpfjgk3rxL9DW87eQ"
"""
默认
refresh_token: aLLNMJ4uFmqmj0seVbY62Xjv00Dpfjgk3rxL9DW87eQ
"""


class Pixiv:
    def __init__(self, refresh_token: str, pass_gfw=True):
        if pass_gfw:
            try:
                self.api = ByPassSniApi()  # Same as AppPixivAPI, but bypass the GFW
                self.api.require_appapi_hosts()
            except Exception as e:
                self.api = None
                print(e)

        else:
            try:
                self.api = AppPixivAPI()
            except Exception as e:
                try:
                    self.api = ByPassSniApi()  # Same as AppPixivAPI, but bypass the GFW
                    self.api.require_appapi_hosts()
                except Exception as e:
                    self.api = None
                    print(e)
                print(e)

        try:
            self.api.auth(refresh_token=refresh_token)
        except Exception as e:
            print(e)
            self.api = None

    def download(self, url: str, directory: str = "Pixiv/", filename: str = "tmp.jpg"):
        if not os.path.exists(directory):
            os.makedirs(directory)

        self.api.download(url, directory, fname=filename)

    def get_illust(self, illust_id):
        illust = self.api.illust(illust_id)
        return illust

    def get_illust_recommended(self, req_auth=True, bookmark_illust_ids=112075876):
        if req_auth:
            return self.api.illust_recommended(req_auth=req_auth).illusts
        return self.api.illust_recommended(
            req_auth=req_auth, bookmark_illust_ids=bookmark_illust_ids
        ).illusts

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
        hh = self.get_illust_detail(illust_id).illust
        print(str(hh) + "\n")
        return self.get_illust_detail(illust_id).illust.image_urls[size]

    def get_illust_original_url(self, illust_id: int):
        hh = self.get_illust_detail(
            illust_id
        ).illust.meta_single_page.original_image_url
        print(str(hh) + "\n")
        return self.get_illust_detail(
            illust_id
        ).illust.meta_single_page.original_image_url


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


pixiv = None


class PixivThread(threading.Thread):
    def __init__(self, refresh_token):
        super(PixivThread, self).__init__()
        self.refresh_token = refresh_token
        self._stop_event = threading.Event()  # Event to signal the thread to stop

    def run(self):
        while not self._stop_event.is_set():
            global pixiv
            pixiv = Pixiv(self.refresh_token)
            if pixiv.api is not None:
                print("Pixiv插件启动成功！\n")
                break
            else:
                print("Pixiv插件启动失败！\n")
            time.sleep(1)

    def stop(self):
        self._stop_event.set()  # Set the stop event to signal the thread to stop
        self.join()  # Wait for the thread to complete

    def restart(self):
        self._stop()  # Stop the current thread
        self.__init__(self.refresh_token)  # Reinitialize the thread
        self.start()  # Start the new thread


# 假设 Pixiv 类已经定义了，你需要替换为实际的 Pixiv 类

# 在主线程中创建并启动 PixivThread

pixiv_thread = PixivThread(_REFRESH_TOKEN)
pixiv_thread.start()


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
                "pid: ",
            ]

            pid_search_start_index = -1

            for cmd in pid_cmd:
                if cmd in content:
                    pid_search_start_index = content.find(cmd)
                    pid_search_start_index += len(cmd)
                    break

            one_pic_cmd = ["来张色图", "来张涩图", "来点色图", "来点涩图", "色图", "涩图"]

            one_pic_start_index = -1

            for cmd in one_pic_cmd:
                if cmd in content:
                    one_pic_start_index = content.find(cmd)
                    one_pic_start_index += len(cmd)
                    break

            if one_pic_start_index != -1:
                try:
                    recommends = pixiv.get_illust_recommended()
                    i = 0
                    while not recommends or i < 2:
                        print("获取推荐图片失败\n")
                        pixiv_thread.restart()
                        recommends = pixiv.get_illust_recommended()
                        i = i + 1
                    size = len(recommends)
                    index = random.randint(0, size - 1)
                    pid = recommends[index].id
                    pic_url = pixiv.get_illust_original_url(pid)
                    i = 0
                    while not pic_url or i < 2:
                        pixiv_thread.restart()
                        print("获取图片链接失败\n")
                        pic_url = pixiv.get_illust_original_url(pid)
                        i = i + 1
                    if (not pic_url) or (not recommends):
                        send_message(
                            TextMessage(
                                message.getEventData().FromUin(),
                                message.getEventData().FromType(),
                                "获取图片失败",
                            )
                        )
                    title = pixiv.get_illust_detail(pid).illust.title
                    title_s = title.replace("/", "·")
                    title_s = title.replace('"', "+")
                    author_name = pixiv.get_illust_detail(pid).illust.user.name
                    author_name_s = author_name.replace("/", "-")
                    author_name_s = author_name.replace('"', "=")
                    tags_jsons = pixiv.get_illust_detail(pid).illust.tags

                    tags = ""
                    file_type = None
                    if pic_url.find("jpg") != -1:
                        file_type = "jpg"
                    elif pic_url.find("png") != -1:
                        file_type = "png"
                    fileName_ = f"{author_name_s}_{title_s}_{pid}.{file_type}"
                    directory = "Pixiv/img/"
                    if os.path.isfile(directory + fileName_) is False:
                        pixiv.download(pic_url, directory=directory, filename=fileName_)
                    pic_path = f"{directory}" + f"{fileName_}"
                    for i in tags_jsons:
                        tags += "#" + i.name + "\n"
                    InfoText = f"""标题：\n{title}\n\n作者:\n{author_name}\n\npid:\n{pid}\n\nurl:\nhttps://www.pixiv.net/artworks/{pid}\n\ntags:\n{tags}"""
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

            if pid_search_start_index != -1:
                try:
                    pid = int(content[pid_search_start_index:])
                    pic_url = pixiv.get_illust_original_url(pid)
                    i = 0
                    while not pic_url or i < 2:
                        print("获取图片失败\n")
                        pixiv_thread.restart()
                        pic_url = pixiv.get_illust_original_url(pid)
                        i += 1
                    if not pic_url:
                        send_message(
                            TextMessage(
                                message.getEventData().FromUin(),
                                message.getEventData().FromType(),
                                "获取图片失败",
                            )
                        )
                    title = pixiv.get_illust_detail(pid).illust.title
                    title_s = title.replace("/", "·")
                    title_s = title.replace('"', "+")
                    author_name = pixiv.get_illust_detail(pid).illust.user.name
                    author_name_s = author_name.replace("/", "-")
                    author_name_s = author_name.replace('"', "+")
                    tags_jsons = pixiv.get_illust_detail(pid).illust.tags

                    tags = ""
                    file_type = None
                    if pic_url.find("jpg") != -1:
                        file_type = "jpg"
                    elif pic_url.find("png") != -1:
                        file_type = "png"
                    fileName_ = f"{author_name_s}_{title_s}_{pid}.{file_type}"
                    directory = "./Pixiv/img/"
                    if os.path.isfile(directory + fileName_) is False:
                        pixiv.download(pic_url, directory=directory, filename=fileName_)
                    pic_path = f"{directory}" + f"{fileName_}"
                    for i in tags_jsons:
                        tags += "#" + i.name + "\n"
                    InfoText = f"""标题：\n{title}\n\n作者:\n{author_name}\n\npid:\n{pid}\n\nurl:\nhttps://www.pixiv.net/artworks/{pid}\n\ntags:\n{tags}"""
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
