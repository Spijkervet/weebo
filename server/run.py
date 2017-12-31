import os

from app import create_app

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database.db")

app = create_app(DB_PATH)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4000, debug=True)
