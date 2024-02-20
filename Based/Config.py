import yaml


def get_config(yaml_file_path: str):
    with open(yaml_file_path, "r", encoding="utf-8") as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data


Bot_Config = get_config("Config/config.yaml")

config_data = Bot_Config
Host = config_data["Host"]
QQBotUid = config_data["QQBotUid"]
devicename = config_data["devicename"]
Myjson = config_data["json"]
send_forbidden = config_data["send_forbidden"]
receive_forbidden = config_data["receive_forbidden"]
super_users = config_data["super_users"]
BotToken = config_data["BotToken"]
