import json
import datetime
import time
from Based.Message import TextMessage
from Based.Send_Message import send_message
from Based.Config import config_data


def load_check_in_data():
    try:
        with open("data/check_in.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_check_in_data(data):
    with open("data/check_in.json", "w") as file:
        json.dump(data, file, indent=4)


def check_in():
    check_in_config = config_data["checkin"]
    check_in_data = load_check_in_data()

    while True:
        current_date = str(datetime.datetime.now().date().strftime("%Y-%m-%d"))

        for i in check_in_config:
            group = list(i.keys())[0]
            message = i[group]

            last_check_in_date = check_in_data.get(str(group))
            if last_check_in_date is None or last_check_in_date != current_date:
                check_in_data[str(group)] = current_date
                save_check_in_data(check_in_data)
                send_message(TextMessage(group, 2, message))

        time.sleep(60 * 60 * 24)
