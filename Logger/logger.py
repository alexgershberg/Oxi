from flask import Flask, request
import logging
import os


app = Flask(__name__)
logging.getLogger('werkzeug').disabled = True


@app.route('/log', methods=['POST'])
def log():
    yell_json: dict = request.get_json()
    broadcast(yell_json)
    return 'eeee'


def broadcast(request_json: dict):
    username = request_json['username']
    message = request_json['message']
    time = request_json['time']
    print(f'APP [{request_json["app_node"]}] | LOG [{os.uname().nodename}]', flush=True)
    print(f'[{time}] {username}{message}', flush=True)
