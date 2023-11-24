import requests
import base64
from PIL import Image
from io import BytesIO
from Based.QR_Cout import print_QR
import requests


def login_QQ(get_config):
    Host = get_config["Host"]
    QQBotUid = get_config["QQBotUid"]
    devicename = get_config["devicename"]
    json = get_config["json"]
    login_url = "http://{}/v1/login/getqrcode?qq={}&devicename={}&json={}".format(
        Host, QQBotUid, devicename, json
    )
    payload = {}
    headers = {"User-Agent": "Apifox/1.0.0 (https://apifox.com)"}

    response = requests.get(login_url, headers=headers, data=payload)

    """print(response.text)
    """
    response_json = response.json()

    bqbase64rpic = response_json["ResponseData"]["BQBase64rpic"]
    ##print(bqbase64rpic)

    # 将 BQBase64rpic 的内容解码为二进制数据
    bqbinary = base64.b64decode(bqbase64rpic)

    # 将二进制数据转换为图片对象
    bqimage = Image.open(BytesIO(bqbinary))

    bqimage.save("QR.png")
    qr_code = Image.open("QR.png")
    # 旧的打印函数不要了
    # print_QR(qr_code)
    print_QR(response_json["ResponseData"]["QrUrl"])
