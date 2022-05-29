import os
import datetime
import sys
import redis
from oxi_json_typing import T_Response_Json, T_Yell_Json, T_Enquiry_Json
from typing import Dict, Optional
from flask import Flask, request
import requests


app = Flask(__name__)
database = redis.Redis(host="redis", port=6379)


@app.route("/yell", methods=["POST"])
def yell_endpoint():
    yell_json: T_Yell_Json = request.get_json()

    try:
        current_index = database.hincrby("index", "count")
        yell_json["index"] = f"{current_index}"
        yell_json["time"] = f"{datetime.datetime.now().strftime('%x %X')}"
        database.hset(current_index, mapping=yell_json)
    except Exception:
        print("Error. No access to database.", file=sys.stderr)

    yell_json["app_node"] = f"{os.uname().nodename}"

    try:
        requests.post("http://logger:2515/log", json=yell_json)
    except Exception:
        pass

    return ""


@app.route("/hear", methods=["GET"])
def hear_endpoint() -> T_Response_Json:
    enquiry_json: T_Enquiry_Json = request.get_json()
    enquiry_index: str = enquiry_json["index"]
    enquiry_max_load: int = int(enquiry_json["max_load"])
    db_index: Optional[bytes] = None
    try:
        db_index: Optional[bytes] = database.hget("index", "count")
    except Exception as e:
        print("Error. Database not found. Is Redis running?")

    response_json: T_Response_Json = assemble_response_json(enquiry_index, db_index, enquiry_max_load)
    return response_json


def assemble_response_json(enquiry_index: str, db_index: Optional[bytes], enquiry_max_load: int) -> T_Response_Json:
    if db_index is None:
        return {"db_index": "0", "message_count": "0", "container": f"{os.uname().nodename}", "records": {}}

    enquiry_index: int = int(enquiry_index)
    db_index: int = int(db_index)

    if enquiry_index == db_index:
        return {"db_index": f"{db_index}", "message_count": "0",  "container": f"{os.uname().nodename}", "records": {}}

    records_count = db_index - enquiry_index
    if records_count >= enquiry_max_load:
        enquiry_index = db_index - enquiry_max_load

    records: Dict[str, str] = {}

    for i in range(enquiry_index + 1, db_index + 1):
        # Database return type needs to be checked. Not sure if its always Dict[str, str] (or, if it can be None)
        data: Optional[Dict[str, str]] = database.hgetall(i)
        if data:
            # Not sure why i'm getting this warning. Have to check type-correctness.
            records[f"{i}"] = f"{data}"

    response_json: T_Response_Json = {
        "db_index": f"{db_index}",
        "message_count": f"{db_index - enquiry_index}",
        "container": f"{os.uname().nodename}",
        "records": records
    }

    return response_json
