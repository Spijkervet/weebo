from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort
from instance.config import app_config

# initialize sql-alchemy
db = SQLAlchemy()

def create_app(config_name):

    from app.models import Alarm

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route("/alarms/", methods=['POST', 'GET'])
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

    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    return app
