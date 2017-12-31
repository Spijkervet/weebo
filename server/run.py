import os

from app import create_app

app = create_app("testing")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
