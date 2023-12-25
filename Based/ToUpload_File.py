"""   
command_id 1好友图片 2群组图片 26好友语音 29群组语音

way 有一下三种：

FilePath  文件本地路径FilePath, FileUrl、Base64Buf不能同时存在

FileUrl 文件网络路径

Base64Buf Base64Buf编码

path 是文件路径或者文件网络路径或者Base64Buf编码
"""
import time
import requests
import json
from Based.Config import get_config
from PIL import Image
import requests
from io import BytesIO
import base64

config = "Config/config.yaml"
config_data = get_config(config)  # Renamed the variable to avoid conflict
Host = config_data["Host"]
QQBotUid = config_data["QQBotUid"]
devicename = config_data["devicename"]
Myjson = config_data["json"]


def get_image_size(path: str):
    if path.startswith("http"):
        # 如果是图片链接
        response = requests.get(path)
        img = Image.open(BytesIO(response.content))
    elif path.startswith("data:image"):
        # 如果是 base64 编码的图片数据
        encoded_data = path.split(",")[1]
        decoded_data = base64.b64decode(encoded_data)
        img = Image.open(BytesIO(decoded_data))
    else:
        # 如果是文件路径
        img = Image.open(path)

    width, height = img.size
    return width, height


class UpFile:
    """
    command_id 1好友图片 2群组图片 26好友语音 29群组语音

    way 有一下三种：

    FilePath  文件本地路径FilePath, FileUrl、Base64Buf不能同时存在

    FileUrl 文件网络路径

    Base64Buf Base64Buf编码

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
        self.__height, self.__width = get_image_size(path)
        self.__info = self.get_info()

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
