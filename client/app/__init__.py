from flask import Flask, request, abort, render_template
from flask_wtf.csrf import CSRFProtect
from .forms import QueryForm
from .weebo import weebo, clean_gpio

app = Flask(__name__)
app.secret_key = "JF*(&#OURIJLKDFSKJSDKLFJSLBNAS)"
def create_app(config_name):
    return app


@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        if(request.form.get("whisper")):
            weebo(query, whisper=True)
        else:
            weebo(query)

    form = QueryForm()
    return render_template('index.html', form=form)


def clean():
    clean_gpio()
