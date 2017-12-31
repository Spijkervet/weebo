import requests
from flask import render_template, Blueprint
from flask_login import login_required, current_user
from .. import app_info
from ..weebo.settings import Settings
index_bp = Blueprint('index', __name__)


@index_bp.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html', app_info=app_info, user=current_user)

@index_bp.route('/settings', methods=['GET'])
def settings():
    return render_template('settings.html', app_info=app_info, user=current_user)

@index_bp.route('/logs', methods=['GET'])
def logs():
    json_response = requests.get("http://" + Settings.weebo_server_address + ":" + Settings.weebo_server_port + "/queries").json()
    return render_template('logs.html', app_info=app_info, user=current_user, queries=json_response)
