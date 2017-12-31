from flask import Flask
from flask_socketio import SocketIO
from .info import Info
from flask_login import LoginManager


from .weebo import Weebo

__version__ = '1.0.0'

app_info = Info()
socketio = SocketIO()
login_manager = LoginManager()

weebo = Weebo()

def create_app(DB_PATH):
    from . import events

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'Aqewur381!%*'

    from .views.index import index_bp
    from .views.login import login_bp
    app.register_blueprint(index_bp)
    app.register_blueprint(login_bp)

    socketio.init_app(app)
    # login_manager.init_app(app)
    return app

def reset():
    weebo.reset()
