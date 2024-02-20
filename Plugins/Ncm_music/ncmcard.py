class NcmCard:
    def __init__(self, info: dict):
        title = info["name"]
        id = info["id"]
        preview = info["al"]["picUrl"]
        card = {
            "app": "com.tencent.structmsg",
            "config": {
                "ctime": 1699495141,
                "forward": 1,
                "token": "07708301a3f6616a96d3658d0a2a9043",
                "type": "normal",
            },
            "desc": "音乐",
            "extra": {
                "app_type": 1,
                "appid": 100495085,
                "msg_seq": 11404322491231877251,
                "uin": 3466484185,
            },
            "meta": {
                "music": {
                    "action": "",
                    "android_pkg_name": "",
                    "app_type": 1,
                    "appid": 100495085,
                    "ctime": 1699495141,
                    "desc": "TimeZ",
                    "jumpUrl": "https://music.163.com/song/?id=" + str(id),
                    "musicUrl": "https://music.163.com/song/media/outer/url?id="
                    + str(id),
                    "preview": preview,
                    "sourceMsgId": "0",
                    "source_icon": "https://i.gtimg.cn/open/app_icon/00/49/50/85/100495085_100_m.png",
                    "source_url": "",
                    "tag": "网易云音乐",
                    "title": title,
                    "uin": 3466484185,
                }
            },
            "prompt": "[分享]" + title,
            "ver": "0.0.0.1",
            "view": "music",
        }
        self.card = str(card)
