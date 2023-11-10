import requests
import json


def post_request(url) -> dict:
    headers = {
        'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers)

    result_json = response.json()
    return result_json


#print(post_request("https://ncmapi.xyr.icu/search?keywords=%E6%B5%B7%E9%98%94%E5%A4%A9%E7%A9%BA"))
