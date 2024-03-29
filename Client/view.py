import ast
import requests
import time
from oxi_json_typing import T_Response_Json, T_Enquiry_Json, T_Yell_Json

hear: str = "http://127.0.0.1:5000/hear"
max_load: int = 100  # Load last N messages (To avoid loading entire message history)


class Data:
    _local_index = 0


def broadcast(response_json: T_Response_Json, local_index: int, db_index: int) -> None:
    message_count = response_json["message_count"]
    if message_count == "0":
        return

    records = response_json["records"]

    for message_index in range(local_index + 1, db_index + 1):
        try:
            current_record: T_Yell_Json = ast.literal_eval(records[str(message_index)])
        except KeyError:
            print(f'[ERROR] KeyError: {message_index}')
            print(f'{records}')

        # Yell_Json keys get encoded into bytes, when we store things into the redis DB.
        # ("time" becomes b"time")
        # Don't know how to get around that just yet
        current_time = current_record[b"time"].decode()
        username = current_record[b"username"].decode()
        message = current_record[b"message"].decode()
        print(f"[{response_json['container']}] ", end="")
        print(f"[{current_time}] {username}{message}")

    Data._local_index = db_index


if __name__ == "__main__":
    while True:
        enquiry_json: T_Enquiry_Json = {
            "index": f"{Data._local_index}",
            "max_load": f"{max_load}"  # Load at most N amount of messages
        }

        time.sleep(1)

        raw_response_json = None



        try:
            raw_response_json = requests.get(hear, json=enquiry_json)
        except Exception as e:
            print("Error while sending a request. Is the server down?")

        if raw_response_json is not None:
            response_json: T_Response_Json = ast.literal_eval(raw_response_json.text)
            #print(f'[DEBUG] {response_json}')
            message_count: int = int(response_json["message_count"])
            db_index: int = int(response_json["db_index"])
            start_index: int = db_index - message_count
            broadcast(response_json, start_index, db_index)
