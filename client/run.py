import os
from app import create_app, clean

app = create_app("testing")

if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0')
    except KeyboardInterrupt:
        print("*** INTERRUPTED ***")
        clean()
