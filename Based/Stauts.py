import requests
import json

# 获取状态


def get_Status(my_config):  # Corrected the function name
    Host = my_config["Host"]
    QQBotUid = my_config["QQBotUid"]
    # devicename = my_config["devicename"]
    url = f"http://{Host}/v1/LuaApiCaller?funcname=MagicCgiCmd&timeout=10&qq={QQBotUid}"

    payload = json.dumps({"CgiCmd": "ClusterInfo", "CgiRequest": {}})
    headers = {
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Content-Type": "application/json",
    }
    import time

    while True:
        try:
            # 尝试执行的代码
            response = requests.request("POST", url, headers=headers, data=payload)
            pass
        except Exception as e:
            print(f"发生错误: {e}")
            print("10秒后重试...")
            time.sleep(10)
        else:
            # 如果没有错误，跳出循环
            break

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)

    # response.json()["CgiBaseResponse"]["Ret"]

    return response.json()["CgiBaseResponse"]["Ret"] == 0
