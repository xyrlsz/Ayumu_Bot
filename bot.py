from Based.Config import get_config
from Based.Login import login_QQ
from Based.Stauts import get_Status
from Based.ToUpload_File import UpFile

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
