import os
import datetime
import redis
from flask import Flask, request
import requests

app = Flask(__name__)
database = redis.Redis(host='redis', port=6379)


@app.route('/yell', methods=['POST'])
def yell_endpoint():
    yell_json = request.get_json()

    try:
        current_index = database.hincrby("index", "count")
        yell_json["index"] = f"{current_index}"
        yell_json["time"] = f"{datetime.datetime.now().strftime('%x %X')}"
        database.hset(current_index, mapping=yell_json)
    except Exception:
        pass

    yell_json["app_node"] = f"{os.uname().nodename}"

    try:
        log_json = requests.post('http://logger:2515/log', json=yell_json)
    except Exception:
        pass

    return 'log_json'


@app.route('/hear', methods=['GET'])
def hear_endpoint():
    enquiry_json = request.get_json()
    enquiry_index: str = enquiry_json["index"]
    db_index: bytes or None = database.hget("index", "count")
    response_json = assemble_response_json(enquiry_index, db_index)
    return response_json


def assemble_response_json(enquiry_index: str, db_index: bytes or None):
    if db_index is None:
        return {"db_index": "0", "message_count": "0", "container": f'{os.uname().nodename}'}

    enquiry_index: int = int(enquiry_index)
    db_index: int = int(db_index)

    if enquiry_index == db_index:
        return {"db_index": f'{db_index}', "message_count": "0",  "container": f'{os.uname().nodename}'}

    response_json = {
        "db_index": f"{db_index}",
        "message_count": f"{db_index - enquiry_index}",
        "container": f'{os.uname().nodename}'
    }

    records = {}
    for i in range(enquiry_index, db_index + 1):
        data = database.hgetall(i)
        if data:
            records[f"{i}"] = f'{data}'

    response_json["records"] = records

    return response_json
