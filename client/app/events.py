import sys, json
from datetime import datetime

from flask import session
from flask_socketio import emit
from . import socketio

def get_server_data():
    data = {}
    data["version"] = sys.version
    data["time"] = datetime.now().strftime("%m/%d/%Y, %I:%M:%S%p")
    return data

def send_data():
    data = get_server_data()
    emit("update", json.dumps(data))

@socketio.on('connected')
def connection_handler(data):
    pong(data)

@socketio.on('ping')
def pong(data):
    send_data()
    emit("pong")


@socketio.on('consoleMessage')
def console_message(data):
    from . import weebo
    from .weebo.data import WeeboData
    print(data)
    weebo_data = WeeboData()
    weebo_data.query = data["message"]
    weebo_data.api = data["api"]
    weebo_data.say = data["button"] == "say"
    weebo.process(weebo_data)
