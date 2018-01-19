import json
import os

from flask import Flask, request, abort, send_file, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

from . import brain


#from app.models import Alarm

# initialize sql-alchemy

app = Flask(__name__)

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(DB_PATH):

    from . import models

    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + DB_PATH
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    bcrypt.init_app(app)
    #from .auth import auth_blueprint
    #app.register_blueprint(auth_blueprint)
    return app


@app.route("/query/", methods=['GET'])
def query():



    print("API: " + request.args.get('api'))
    if(request.args.get('data')):
        if(request.args.get('whisper') == "True"):
            #task = multiprocessing.Process(target=brain.process, args=(request.args.get('data'), request.args.get('api')))
            #task.start()
            filename = brain.process(request.args.get('data'), api=request.args.get('api'), whisper=True)
        else:
            # task = multiprocessing.Process(target=brain.process, args=(request.args.get('data'), request.args.get('api')))
            #task.start()
            filename = brain.process(request.args.get('data'), api=request.args.get('api'))
        return send_file(filename, mimetype='audio/mpeg')
    return "", 401;

@app.route("/say/", methods=['GET'])
def say():
    if(request.args.get('data')):
        if(request.args.get('whisper') == "True"):
            filename = brain.say(request.args.get('data'), whisper=True)
        else:
            filename = brain.say(request.args.get('data'))
        return send_file(filename, mimetype='audio/mpeg')
    return "", 401;


@app.route("/queries/", methods=['GET'])
def queries():
    from .models import Queries
    queries = Queries.query.all()
    d = []
    for query in queries:
        q_dict = query.__dict__.copy()
        del q_dict['_sa_instance_state']
        q_dict['date_created'] = str(q_dict['date_created'])
        d.append(q_dict)
    return json.dumps(d)

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


# webhook
@app.route('/webhook', methods=['POST'])
def webhook():

    req = request.get_json(silent=True, force=True)
    print("RECeEEEIVVEED ", req)
    print(json.dumps(req, indent=4))
    res = processRequest(req)
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "yahooWeatherForecast":
        return {}
    baseurl = "https://query.yahooapis.com/v1/public/yql?"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + urlencode({'q': yql_query}) + "&format=json"
    result = urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "') and u='c'"


def makeWebhookResult(data):
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

    speech = "Today the weather in " + location.get('city') + ": " + condition.get('text') + \
             ", And the temperature is " + condition.get('temp') + " " + units.get('temperature')

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }
