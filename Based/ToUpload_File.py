"""   
command_id 1好友图片 2群组图片 26好友语音 29群组语音

way 有一下三种：

FilePath  文件本地路径FilePath, FileUrl、Base64Buf不能同时存在

FileUrl 文件网络路径

Base64Buf Base64Buf编码

path 是文件路径或者文件网络路径或者Base64Buf编码
"""

import base64
import io
import json
import time
import base64
from io import BytesIO

import requests
from PIL import Image
from PIL import UnidentifiedImageError

from Based.Config import Host, QQBotUid


def image_to_base64(image_path: str) -> str:
    with open(image_path, "rb") as image_file:
        # 读取图片文件的二进制数据
        image_binary = image_file.read()
        # 使用base64编码
        base64_encoded = base64.b64encode(image_binary).decode("utf-8")
        return base64_encoded


def img_url_to_based64(url: str) -> str:
    try:
        response = requests.get(url)
        response.raise_for_status()
        image_base64 = base64.b64encode(response.content).decode("utf-8")
        return image_base64

    except Exception as e:
        print(f"Error: {e}")

    return ""


def is_image_from_url(url: str):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with Image.open(io.BytesIO(response.content)) as img:
            img.verify()
            return True
    except UnidentifiedImageError:
        return False
    except Exception as e:
        # print(f"An error occurred: {e}")
        return False


def is_image_from_base64(base64_data: str):
    try:
        img_data = base64.b64decode(base64_data)
        with Image.open(io.BytesIO(img_data)) as img:
            img.verify()
            return True
    except UnidentifiedImageError:
        return False
    except Exception as e:
        # print(f"An error occurred: {e}")
        return False


def is_image_from_filePath(file_path: str):
    try:
        with Image.open(file_path) as img:
            img.verify()
            return True
    except UnidentifiedImageError:
        return False
    except Exception as e:
        # print(f"An error occurred: {e}")
        return False


def is_image(path: str) -> bool:
    return (
        is_image_from_url(path)
        or is_image_from_base64(path)
        or is_image_from_filePath(path)
    )


def get_image_size(path: str) -> list:
    try:
        if is_image_from_url(path):
            # 如果是图片链接
            response = requests.get(path)
            response.raise_for_status()  # 检查请求是否成功
            img = Image.open(BytesIO(response.content))
        elif is_image_from_base64(path):
            # 如果是 base64 编码的图片数据
            encoded_data = path
            decoded_data = base64.b64decode(encoded_data)
            img = Image.open(BytesIO(decoded_data))
        elif is_image_from_filePath(path):
            # 如果是文件路径
            img = Image.open(path)

        width, height = img.size
        return width, height
    except Exception as e:
        # 捕获所有异常，打印错误信息，可以根据实际情况修改处理方式
        print(f"Error in get_image_size: {e}")
        return 0, 0  # 返回默认值或者适当的错误处理


class UpGroupFile:
    """
    path 是文件路径或者文件网络路径或者Base64Buf编码

    FilePath, FileUrl、FileBase64不能同时存在

    FilePath  文件本地路径

    FileUrl 文件网络路径

    FileBase64 Base64Buf编码

    """

    def __init__(self, path: str, group_id: int, file_name: str, command_id: int = 71):
        self.command_id = command_id
        self.path = path
        self.__body = {
            "CgiCmd": "PicUp.DataUp",
            "CgiRequest": {
                "CommandId": 71,
                "FileName": file_name,
                "FilePath": path,
                "Notify": True,
                "ToUin": group_id,
            },
        }

    def upload(self):
        url = "http://{}/v1/upload?qq={}".format(Host, QQBotUid)

        payload = json.dumps(self.__body)  # Use the constructed body

        headers = {
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
            "Content-Type": "application/json",
        }

        while True:
            try:
                # 尝试执行的代码
                requests.post(url, headers=headers, data=payload)
                pass
            except Exception as e:
                print(f"发生错误: {e}")
                print("10秒后重试...")
                time.sleep(10)
            else:
                # 如果没有错误，跳出循环
                break


class UpFile:
    """
    command_id 1好友图片 2群组图片 26好友语音 29群组语音

    way 有一下三种：

    FilePath  文件本地路径FilePath, FileUrl、FileBase64不能同时存在

    FileUrl 文件网络路径

    FileBase64 Base64Buf编码

    path 是文件路径或者文件网络路径或者Base64Buf编码"""

    def __init__(self, command_id: int, way: str, path: str):
        self.__command_id = command_id
        # self.__is_Uplaoded = False
        self.__height, self.__width = 0, 0
        if way == "FilePath":
            self.__body = {
                "CgiCmd": "PicUp.DataUp",
                "CgiRequest": {
                    "CommandId": command_id,
                    "FilePath": path,
                },
            }
            # if self.__command_id == 1 or self.__command_id == 2:
            #     self.__height, self.__width = Image.open(path).size
        elif way == "FileUrl":
            self.__body = {
                "CgiCmd": "PicUp.DataUp",
                "CgiRequest": {
                    "CommandId": command_id,
                    "FileUrl": path,
                },
            }
            # if self.__command_id == 1 or self.__command_id == 2:
            #     response = requests.get(path)

            #     if response.status_code == 200:
            #         image_data = BytesIO(response.content)
            #         img = Image.open(image_data)
            #     self.__height, self.__width = img.size
        elif way == "FileBase64":
            self.__body = {
                "CgiCmd": "PicUp.DataUp",
                "CgiRequest": {
                    "CommandId": command_id,
                    "Base64Buf": path,
                },
            }
            # bqbinary = base64.b64decode(path)
            # bqimage = Image.open(BytesIO(bqbinary))
            # self.__height, self.__width = bqimage.size
        if is_image(path):
            self.__width, self.__height = get_image_size(path)
        self.__info = self.get_info()
        print(self.__info)

    def get_body(self) -> dict:
        return self.__body

    def get_info(self) -> dict:
        url = "http://{}/v1/upload?qq={}".format(Host, QQBotUid)

        payload = json.dumps(self.__body)  # Use the constructed body

        headers = {
            "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
            "Content-Type": "application/json",
        }

        while True:
            try:
                # 尝试执行的代码
                response = requests.post(url, headers=headers, data=payload)
                pass
            except Exception as e:
                print(f"发生错误: {e}")
                print("10秒后重试...")
                time.sleep(10)
            else:
                # 如果没有错误，跳出循环
                break

        # if response.json()["CgiBaseResponse"]["Ret"] == 0 and self.is_Uplaoded == False:
        #     print("上传成功")
        # else:
        #     print("上传失败")
        # print(response.text)
        # if self.__is_Uplaoded == False:
        #     self.__is_Uplaoded = True
        return response.json()

    def get_file_md5(self) -> str:
        if self.__info["ResponseData"]["FileMd5"]:
            return self.__info["ResponseData"]["FileMd5"]
        return ""

    def get_file_id(self) -> int:
        if self.__command_id == 1 or self.__command_id == 2:
            return self.__info["ResponseData"]["FileId"]
        return -1

    def get_file_size(self) -> int:
        if self.__info["ResponseData"]["FileSize"]:
            return self.__info["ResponseData"]["FileSize"]
        return -1

    def get_file_token(self) -> str:
        if self.__command_id == 26 or self.__command_id == 29:
            return self.__info["ResponseData"]["FileToken"]
        return ""

    def get_height(self) -> int:
        return self.__height

    def get_width(self) -> int:
        return self.__width


# file = UpFile(
#     2, "FileUrl", "https://pic1.zhimg.com/v2-e0ca937a1d3296e7463aa0aa096bef48_r.jpg"
# )
# print(file.get_file_md5())
# print(file.get_file_id())
# print(file.get_file_size())
