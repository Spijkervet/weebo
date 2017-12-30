import os.path
from app import create_app, socketio
from celery import Celery

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app = create_app(DB_PATH)
app.host = '127.0.0.1'
app.debug = True


def cef():
    from cefpython3 import cefpython as cef
    import platform
    import sys

    # check_versions()
    sys.excepthook = cef.ExceptHook  # To shutdown all CEF processes on error
    cef.Initialize()
    cef.CreateBrowserSync(url="https://www.youtube.com/",
                          window_title="Hello World!")
    cef.MessageLoop()
    cef.Shutdown()


if __name__ == '__main__':
    # celery = make_celery(app)
    # cef()
    socketio.run(app)
