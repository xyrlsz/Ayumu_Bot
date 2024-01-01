import time

import requests


def post_request(url) -> dict:
    headers = {
        "User-Agent": "Apifox/1.0.0 (https://apifox.com)",
        "Content-Type": "application/json",
    }

    while True:
        try:
            # 尝试执行的代码
            response = requests.request("POST", url, headers=headers)

            pass
        except Exception as e:
            print(f"发生错误: {e}")
            print("10秒后重试...")
            time.sleep(10)
        else:
            # 如果没有错误，跳出循环
            break
    result_json = response.json()
    return result_json


# print(post_request("https://ncmapi.xyr.icu/search?keywords=%E6%B5%B7%E9%98%94%E5%A4%A9%E7%A9%BA"))
