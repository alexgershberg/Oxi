import ast
import requests
import time

hear = 'http://0.0.0.0:5000/hear'


class Data:
    _local_index = 0


def broadcast(data, local_index: int, db_index: int):
    message_count = data['message_count']
    if message_count == '0':
        return

    records: dict = data['records']

    for message_index in range(local_index + 1, db_index + 1):
        current_record = ast.literal_eval(records[str(message_index)])
        time = current_record[b'time'].decode()
        username = current_record[b'username'].decode()
        message = current_record[b'message'].decode()
        # print(f'[{time}] {username}{message}')
        if "container" in data:
            print(f'[{data["container"]}] ', end='')
        print(f'[{time}] {username}{message}')

    Data._local_index = db_index


if __name__ == '__main__':
    while True:
        enquiry_json = {
            'index': f'{Data._local_index}'
        }

        time.sleep(0.5)

        response_json = None
        try:
            response_json = requests.get(hear, json=enquiry_json)
        except Exception as e:
            print('Error while sending a request. Is the server down?')

        if response_json is not None:
            data = ast.literal_eval(response_json.text)
            db_index = data['db_index']
            db_index = int(db_index)
            broadcast(data, Data._local_index, db_index)
