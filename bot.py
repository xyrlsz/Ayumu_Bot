import requests
import base64
from PIL import Image
from io import BytesIO
import requests
import json
from Based.Stauts import get_Status
from Based.Login import login_QQ
from Based.Config import get_config
from Based.Message import TextMessage
from Based.Message import ImageMessage
from Based.Message import VoiceMessage
from Based.Message import NormalMessage
from Based.Message import TextWithImageMessage
from Based.Message import CardMessage
from Based.Send_Message import send_message
from Based.ToUpload_File import UpFile
from Based.Activity import Ban_Member

config = "Config/config.yaml"
get_config = get_config(config)

if get_Status(get_config):
    print("已登录")
else:
    print("未登录")
    login_QQ(get_config)


# Ban_Member(791649367, "u_dlIWCAVxm-GV27wBVz8SFg", 10)

new_dict_array = [
    {"Nick": "XYR⊙LSZ ", "Uin": 2434221948},
]

voice = UpFile(26, "FilePath", "data/audio/niganma.amr")

send_message(
    VoiceMessage(
        2434221948,
        1,
        voice.get_file_md5(),
        voice.get_file_size(),
        voice.get_file_token(),
    )
)
# send_message(TextMessage(797649367, 2, "shabi", new_dict_array))
# # message = TextMessage(797649367, 2, "shabi", new_dict_array)

# message = TextMessage(797649367, 2, "shabi")
# message = TextWithImageMessage(
#     797649367, 2, "shabi", "GJS9JXPGY0Tms46AAVoQ2A==", 2493098788, 716, 1146
# )
# send_message(message)
# img_file = UpFile(2, "FilePath", "QR.png")
# img_message = ImageMessage(
#     797649367,
#     2,
#     img_file.get_file_md5(),
#     img_file.get_file_id(),
#     img_file.get_height(),
#     img_file.get_width(),
# )

# img = ImageMessage(2434221948, 1, img_file.get_file_md5())
# print(img.get_body())
# print(img_file.get_file_md5())
# voice_file = UpFile(29, "FilePath", "ambient-piano-logo-165357.mp3")

# voice_message = VoiceMessage(
#     797649367,
#     2,
#     voice_file.get_file_md5(),
#     voice_file.get_file_size(),
#     voice_file.get_file_token(),
# )
# # print(voice_file.get_file_md5())
# # print(voice_file.get_file_size())
# # print(voice_file.get_file_token())
# send_message(voice_message)


# msg = {
#     "CgiCmd": "MessageSvc.PbSendMsg",
#     "CgiRequest": {
#         "ToUin": 2434221948,
#         "ToType": 1,
#         "Content": "你好",
#         "Images": [{"FileMd5": "ZMj7Nx8q9PojeVGcYETM3g==", "FileSize": 544988}],
#         # "Video": {
#         #     "FileMd5": "yyYmhuZChF7m3M486vG8jw==",
#         #     "FileSize": 1732142,
#         #     "Url": "30510201000436303402010002049117477c02037a1afd02042f2a56310204654a5a3a0410cb262686e642845ee6dcce3ceaf1bc8f02037a1db902010004140000000866696c65747970650000000431303031",
#         # },
#     },
# }
# send_message(NormalMessage(msg))

# send_message(TextMessage(2434221948, 1, "你好"))

# img = UpFile(
#     1,
#     "FileUrl",
#     f"https://ts1.cn.mm.bing.net/th/id/R-C.c5516c2de39e348abadf13bdc2e9de13?rik=GPQec4yVU2FTzg&riu=http%3a%2f%2fpic.bizhi360.com%2fbpic%2f16%2f1416.jpg&ehk=NS%2f9OBR0rFSeQ54WKF5UYxcSm1dzPs%2bXkREdo0DXFQ4%3d&risl=&pid=ImgRaw&r=0",
# )
# send_message(TextWithImageMessage(2434221948, 1, "你好", img.get_file_md5()))


# card = {
#     "app": "com.tencent.structmsg",
#     # "config": {
#     #     "ctime": 1700108202,
#     #     "forward": 1,
#     #     "token": "d3e07056a2ad60271da4dd715dcca020",
#     #     "type": "normal",
#     # },
#     "desc": "音乐",
#     "extra": {
#         "app_type": 1,
#         "appid": 100495085,
#         "msg_seq": 5882158776524690553,
#         "uin": 3466484185,
#     },
#     "meta": {
#         "music": {
#             "action": "",
#             "android_pkg_name": "",
#             "app_type": 1,
#             "appid": 100495085,
#             "ctime": 1700108202,
#             "desc": "尤长靖",
#             "jumpUrl": "https://music.163.com/song/?id=2099338221",
#             "musicUrl": "https://music.163.com/song/media/outer/url?id=2099338221",
#             "preview": "http://p2.music.126.net/Qxm3vHR_p0R-0m944NYGeg==/109951169052573329.jpg",
#             "sourceMsgId": "0",
#             "source_icon": "https://i.gtimg.cn/open/app_icon/00/49/50/85/100495085_100_m.png",
#             "source_url": "",
#             "tag": "网易云音乐",
#             "title": "昨日青空",
#             "uin": 3466484185,
#         }
#     },
#     "prompt": "[分享]昨日青空",
#     "ver": "0.0.0.1",
#     "view": "music",
# }


# card_str = json.dumps(card)

# send_message(CardMessage(2434221948, 1, card_str))
