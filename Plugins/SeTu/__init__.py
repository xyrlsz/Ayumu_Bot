import os
import sys
import threading
import time
import random

from pixivpy3 import AppPixivAPI, ByPassSniApi
from Based.Event import Event
from Based.Message import TextWithImageMessage, TextMessage
from Based.Send_Message import send_message
from Based.ToUpload_File import UpFile, UpGroupFile

sys.dont_write_bytecode = True


_REFRESH_TOKEN = "aLLNMJ4uFmqmj0seVbY62Xjv00Dpfjgk3rxL9DW87eQ"
"""
默认
refresh_token: aLLNMJ4uFmqmj0seVbY62Xjv00Dpfjgk3rxL9DW87eQ
"""


class Pixiv:
    def __init__(self, refresh_token: str, pass_gfw=False):
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
        hh = self.get_illust_detail(illust_id).illust.image_urls[size]
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
    return any(cmd in user_input for cmd in command_list)


def replace_special_characters(input_string: str) -> str:
    special_characters = ["/", "\\", ":", "*", "?", '"', "<", ">", "|"]
    return "".join("_" if char in special_characters else char for char in input_string)


# Pixiv initialization thread
class PixivThread(threading.Thread):
    def __init__(self, refresh_token):
        super().__init__()
        self.refresh_token = refresh_token
        self._stop_event = threading.Event()

    def run(self):
        global pixiv
        pixiv = Pixiv(self.refresh_token)
        if pixiv.api is not None:
            print("Pixiv插件启动成功！\n")
        else:
            print("Pixiv插件启动失败！\n")
        time.sleep(1)

    def stop(self):
        global pixiv
        pixiv = None
        self._stop_event.set()
        self.join()

    async def restart(self):
        self._stop()
        self.__init__(self.refresh_token)
        self.start()


# Pixiv initialization
pixiv_thread = PixivThread(_REFRESH_TOKEN)
pixiv_thread.start()

pixiv = None


# Pixiv image retrieval function
async def SeTu(message: Event):
    if message.getEventData().isBot:
        return False
    try:
        global pixiv
        pid = None
        content = (
            message.getEventData().Content().strip()
            if message.getEventData().MsgBody()
            else ""
        )

        # Commands
        pid_cmd = ["pid:", "pid搜索", "pid", "https://www.pixiv.net/artworks/", "pid: "]
        one_pic_cmd = ["来张色图", "来张涩图", "来点色图", "来点涩图", "色图", "涩图"]

        pid_search_start_index = next(
            (content.find(cmd) + len(cmd) for cmd in pid_cmd if cmd in content), -1
        )
        one_pic_start_index = next(
            (content.find(cmd) for cmd in one_pic_cmd if cmd in content), -1
        )

        if one_pic_start_index != -1:
            if content in one_pic_cmd:
                try:
                    recommends = pixiv.get_illust_recommended()
                    if recommends:
                        print("获取推荐图片成功\n")
                    else:
                        print("获取推荐图片失败\n")
                        await pixiv_thread.restart()
                        recommends = pixiv.get_illust_recommended()
                        send_message(
                            TextMessage(
                                message.getEventData().FromUin(),
                                message.getEventData().FromType(),
                                "获取推荐图片失败",
                            )
                        )
                        return False

                    index = random.randint(0, len(recommends) - 1)

                    pid = recommends[index].id

                except Exception as e:
                    print(e)
                    return False

        if pid_search_start_index != -1:
            try:
                pid = int(content[pid_search_start_index:])

            except Exception as e:
                print(e)
                return False

        if pid:
            title = pixiv.get_illust_detail(pid).illust.title
            if title == None:
                title = " "
            title_s = replace_special_characters(title)
            author_name = pixiv.get_illust_detail(pid).illust.user.name
            if author_name == None:
                author_name = " "
            author_name_s = replace_special_characters(author_name)
            tags_jsons = pixiv.get_illust_detail(pid).illust.tags
            try:
                if content.find("/U ") != -1:
                    pic_url_original = pixiv.get_illust_original_url(pid)
                    if not pic_url_original:
                        print("获取原图失败\n")
                        await pixiv_thread.restart()
                        pic_url_original = pixiv.get_illust_original_url(pid)
                        send_message(
                            TextMessage(
                                message.getEventData().FromUin(),
                                message.getEventData().FromType(),
                                "获取原图失败",
                            )
                        )
                    else:
                        file_type_ = None
                        if pic_url_original.find("jpg") != -1:
                            file_type_ = "jpg"
                        elif pic_url_original.find("png") != -1:
                            file_type_ = "png"
                        fileName_original = (
                            f"{author_name_s}_{title_s}_{pid}.{file_type_}"
                        )
                        directory_origin = "./Pixiv/img/origin/"
                        pic_path_origin = f"{directory_origin}" + f"{fileName_original}"

                        if not (os.path.isfile(pic_path_origin)):
                            pixiv.download(
                                pic_url_original,
                                directory=directory_origin,
                                filename=fileName_original,
                            )

                        if message.getEventData().FromType() == 2:
                            group_file = UpGroupFile(
                                pic_path_origin,
                                message.getEventData().FromUin(),
                                fileName_original,
                            )
                            group_file.upload()

                pic_url = pixiv.get_illust_url(pid)
                if not pic_url:
                    print("获取图片失败\n")
                    await pixiv_thread.restart()
                    pic_url = pixiv.get_illust_url(pid)
                    send_message(
                        TextMessage(
                            message.getEventData().FromUin(),
                            message.getEventData().FromType(),
                            "获取图片失败",
                        )
                    )
                    return False

                tags = ""
                file_type = None
                if pic_url.find("jpg") != -1:
                    file_type = "jpg"
                elif pic_url.find("png") != -1:
                    file_type = "png"

                fileName_ = f"{author_name_s}_{title_s}_{pid}.{file_type}"

                directory = "./Pixiv/img/large/"
                pic_path = f"{directory}" + f"{fileName_}"

                if not (os.path.isfile(pic_path)):
                    pixiv.download(pic_url, directory=directory, filename=fileName_)

                for i in tags_jsons:
                    tags += "#" + i.name + "\n"
                InfoText = f"""标题：\n{title}\n\n作者:\n{author_name}\n\npid:\n{pid}\n\nurl:\nhttps://www.pixiv.net/artworks/{pid}\n\ntags:\n{tags}"""

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

            except Exception as e:
                print(e)
                send_message(
                    TextMessage(
                        message.getEventData().FromUin(),
                        message.getEventData().FromType(),
                        "获取图片失败",
                    )
                )
                return False

    except Exception as e:
        print(e)
        send_message(
            TextMessage(
                message.getEventData().FromUin(),
                message.getEventData().FromType(),
                "获取图片失败",
            )
        )
        return False
    return False
