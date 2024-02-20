# tpye 1：好友 2：群聊 3：私聊
class TextMessage:
    def __init__(self, receiver: int, type: int, message: str, AtUinLists: dict = None):
        if type != 2:
            self.__body = {
                "CgiCmd": "MessageSvc.PbSendMsg",
                "CgiRequest": {
                    "ToUin": receiver,  # Replace 88888888 with the actual receiver
                    "ToType": type,  # 2 for group; 3 for private chat
                    "Content": message,
                },
            }
        else:
            if AtUinLists is not None:
                self.__body = {
                    "CgiCmd": "MessageSvc.PbSendMsg",
                    "CgiRequest": {
                        "ToUin": receiver,
                        "ToType": type,
                        "Content": " " + message,
                        "AtUinLists": [],
                    },
                }
                self.__body["CgiRequest"]["AtUinLists"].extend(AtUinLists)
            else:
                self.__body = {
                    "CgiCmd": "MessageSvc.PbSendMsg",
                    "CgiRequest": {
                        "ToUin": receiver,  # Replace 88888888 with the actual receiver
                        "ToType": type,  # 2 for group; 3 for private chat
                        "Content": message,
                    },
                }

    def get_body(self):
        return self.__body


class ImageMessage:
    def __init__(
        self,
        receiver: int,
        type: int,
        file_md5: str,
        file_id: int = None,
        Height: int = None,
        Width: int = None,
        file_size: int = None,
    ):
        # if file_size is None:
        #     self.__body = {
        #         "CgiCmd": "MessageSvc.PbSendMsg",
        #         "CgiRequest": {
        #             "ToUin": receiver,  # Replace 88888888 with the actual receiver
        #             "ToType": type,  # 2 for group; 3 for private chat
        #             "Images": [
        #                 {
        #                     "FileMd5": file_md5,
        #                 }
        #             ],
        #         },
        #     }
        # else:
        #     self.__body = {
        #         "CgiCmd": "MessageSvc.PbSendMsg",
        #         "CgiRequest": {
        #             "ToUin": receiver,  # Replace 88888888 with the actual receiver
        #             "ToType": type,  # 2 for group; 3 for private chat
        #             "Images": [
        #                 {
        #                     "FileMd5": file_md5,
        #                     "FileSize": file_size,
        #                 }
        #             ],
        #         },
        #     }

        if type != 2:
            self.__body = {
                "CgiCmd": "MessageSvc.PbSendMsg",
                "CgiRequest": {
                    "ToUin": receiver,  # Replace 88888888 with the actual receiver
                    "ToType": type,  # 2 for group; 3 for private chat
                    "Images": [
                        {
                            "FileMd5": file_md5,
                            "FileSize": file_size,
                        }
                    ],
                },
            }
            # if file_size is not None:
            #     self.__body["CgiRequest"]["Images"][0]["FileSize"] = file_size
        else:
            if file_id is None:
                raise ValueError(
                    "For type 2, file_id, Height, and Width must be provided."
                )
            self.__body = {
                "CgiCmd": "MessageSvc.PbSendMsg",
                "CgiRequest": {
                    "ToUin": receiver,
                    "ToType": 2,
                    "Images": [
                        {
                            "FileId": file_id,
                            "FileMd5": file_md5,
                            "FileSize": file_size,
                            "Height": Height,
                            "Width": Width,
                        }
                    ],
                },
            }

    def get_body(self) -> dict:
        return self.__body


class VoiceMessage:
    def __init__(
        self, receiver: int, type: int, file_md5: str, file_size: int, file_token: str
    ):
        self.__body = {
            "CgiCmd": "MessageSvc.PbSendMsg",
            "CgiRequest": {
                "ToUin": receiver,
                "ToType": type,
                "Voice": {
                    "FileMd5": file_md5,
                    "FileSize": file_size,
                    "FileToken": file_token,
                },
            },
        }

    def get_body(self):
        return self.__body


class NormalMessage:
    def __init__(
        self,
        MsgBody: dict,
    ):
        self.__body = MsgBody

    def get_body(self):
        return self.__body


class TextWithImageMessage:
    def __init__(
        self,
        receiver: int,
        type: int,
        message: str,
        file_md5: str,
        file_id: int = None,
        Height: int = None,
        Width: int = None,
        file_size: int = None,
        AtUinLists: dict = None,
    ):
        if type != 2:
            self.__body = {
                "CgiCmd": "MessageSvc.PbSendMsg",
                "CgiRequest": {
                    "ToUin": receiver,  # Replace 88888888 with the actual receiver
                    "ToType": type,  # 2 for group; 3 for private chat
                    "Content": message,
                    "Images": [
                        {
                            "FileMd5": file_md5,
                            "FileSize": file_size,
                        }
                    ],
                },
            }
        else:
            if AtUinLists is not None:
                self.__body = {
                    "CgiCmd": "MessageSvc.PbSendMsg",
                    "CgiRequest": {
                        "ToUin": receiver,
                        "ToType": type,
                        "Content": " " + message,
                        "Images": [
                            {
                                "FileId": file_id,
                                "FileMd5": file_md5,
                                "FileSize": file_size,
                                "Height": Height,
                                "Width": Width,
                            }
                        ],
                        "AtUinLists": [],
                    },
                }
                self.__body["CgiRequest"]["AtUinLists"].extend(AtUinLists)
            else:
                self.__body = {
                    "CgiCmd": "MessageSvc.PbSendMsg",
                    "CgiRequest": {
                        "ToUin": receiver,  # Replace 88888888 with the actual receiver
                        "ToType": type,  # 2 for group; 3 for private chat
                        "Content": message,
                        "Images": [
                            {
                                "FileId": file_id,
                                "FileMd5": file_md5,
                                "FileSize": file_size,
                                "Height": Height,
                                "Width": Width,
                            }
                        ],
                    },
                }
        # if type != 2:
        #     self.__body = {
        #         "CgiCmd": "MessageSvc.PbSendMsg",
        #         "CgiRequest": {
        #             "ToUin": receiver,  # Replace 88888888 with the actual receiver
        #             "ToType": type,  # 2 for group; 3 for private chat
        #             "Content": message,
        #             "Images": [
        #                 {
        #                     "FileMd5": file_md5,
        #                     "FileSize": file_size,
        #                 }
        #             ],
        #         },
        #     }
        # else:
        #     if file_id is None or Height is None or Width is None:
        #         raise ValueError(
        #             "For type 2, file_id, Height, and Width must be provided."
        #         )
        #     self.__body = {
        #         "CgiCmd": "MessageSvc.PbSendMsg",
        #         "CgiRequest": {
        #             "ToUin": receiver,
        #             "ToType": 2,
        #             "Content": " " + message,
        #             "AtUinLists": [],
        #             "Images": [
        #                 {
        #                     "FileId": file_id,
        #                     "FileMd5": file_md5,
        #                     "FileSize": file_size,
        #                     "Height": Height,
        #                     "Width": Width,
        #                 }
        #             ],
        #         },
        #     }
        #     self.__body["CgiRequest"]["AtUinLists"].extend(AtUinLists)

    def get_body(self):
        return self.__body


class CardMessage:
    def __init__(
        self,
        receiver: int,
        type: int,
        Content: str,
    ):
        self.__body = {
            "CgiCmd": "MessageSvc.PbSendMsg",
            "CgiRequest": {
                "ToUin": receiver,
                "ToType": type,
                "SubMsgType": 51,
                "Content": Content,
            },
        }

    def get_body(self):
        return self.__body
