import json
import os

from flask import Flask, request, abort, send_file, make_response, jsonify

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from . import brain

#from app.models import Alarm

# initialize sql-alchemy
app = Flask(__name__)

def create_app(config_name):

    #from .auth import auth_blueprint
    #app.register_blueprint(auth_blueprint)
    return app


@app.route("/query/", methods=['GET'])
def query():
    print("API: " + request.args.get('api'))
    if(request.args.get('data')):
        if(request.args.get('whisper') == "True"):
            filename = brain.process(request.args.get('data'), api=request.args.get('api'), whisper=True)
        else:
            filename = brain.process(request.args.get('data'), api=request.args.get('api'))
        return send_file(filename, mimetype='audio/mpeg')
    return "", 401;

'''
@app.route("/alarms/", methods=['GET', 'POST'])
def alarms():

    if(request.method == "POST"):
        name = str(request.data.get('name', ''))
        if(name):
            alarm = Alarm(name=name)
            alarm.save()
            response = jsonify({
                'id': alarm.id,
                'name': alarm.name,
                'date_created': alarm.date_created,
                'date_modified': alarm.date_modified,
                'alarm_time': alarm.alarm_time
            })
            response.status_code = 201
            return response
    else:
        alarms = Alarm.get_all()
        results = []

        for alarm in alarms:
            obj = {
                'id': alarm.id,
                'name': alarm.name,
                'date_created': alarm.date_created,
                'date_modified': alarm.date_modified,
                'alarm_time': alarm.alarm_time

            }
            results.append(obj)
        response = jsonify(results)
        response.status_code - 200
        return response
'''


# webhook

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)
    res = process_request(req)
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(jsonify(res))
    r.headers['Content-Type'] = 'application/json'
    return r


def process_request(req):
    if req.get("result").get("action") == "yahooWeatherForecast":
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        yql_query = make_yql_query(req)
        if yql_query is None:
            return {}
        yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
        result = urlopen(yql_url).read().decode('utf-8')
        data = json.loads(result)
        # print(data)
        res = make_webhook_result(data)
        return res
    elif(req.get("result").get("action") == "playMusic"):
        # print("*** MUSIC ***")
        baseurl = "https://query.yahooapis.com/v1/public/yql?"
        spotify_query = make_spotify_query(req)
        if spotify_query is None:
            return {}
        spotify_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
        result = urlopen(yql_url).read().decode('utf-8')
        data = json.loads(result)
        # print(data)
        res = make_webhook_result(data)
        return res

    return {}

def make_spotify_query(req):
    result = req.get("result")
    parameters = result.get("parameters")



def make_yql_query(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def make_webhook_result(data):
    query = data.get('query')
    if query is None:
        return {}

    result = query.get('results')
    if result is None:
        return {}

    channel = result.get('channel')
    if channel is None:
        return {}

    item = channel.get('item')
    location = channel.get('location')
    units = channel.get('units')
    if (location is None) or (item is None) or (units is None):
        return {}

    condition = item.get('condition')
    if condition is None:
        return {}

    # print(json.dumps(item, indent=4))
    #+ units.get('temperature')
    speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
             ", the temperature is " + condition.get('temp') + " degrees Celsius"

    # print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }
