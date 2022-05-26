import requests
from oxi_json_typing import T_Message_Json


class User:
    username = None


yell = "http://0.0.0.0:5000/yell"
hear = "http://0.0.0.0:5000/hear"
auth = "http://0.0.0.0:5000/auth"


if __name__ == "__main__":
    uname = str(input("Choose your username: "))

    join_json: T_Message_Json = {
        "username": f"{uname}",
        "message": " joined the chat!"
    }

    User.username = uname
    try:
        requests.post(yell, json=join_json)
    except Exception as e:
        print("Error while sending a request. Is the server down?")

    while True:
        message = str(input())

        if message.lower() == "exit":
            break

        message_json: T_Message_Json = {
            "username": f"{User.username}",
            "message": f": {message}"
        }

        try:
            requests.post(yell, json=message_json)
        except Exception as e:
            print("Error while sending a request. Is the server down?")