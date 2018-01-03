import os.path
from app import create_app, socketio, reset
# from celery import Celery

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

if __name__ == '__main__':
    # celery = make_celery(app)
    # cef()
    try:
        app = create_app(DB_PATH)
        app.host = "0.0.0.0"
        # app.debug = True
        socketio.run(app, host="0.0.0.0")
    except KeyboardInterrupt:
        print("*** STOPPING SERVICeS ***")
        reset()
