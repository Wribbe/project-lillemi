import os
from flask import render_template, Flask

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


def run():
    os.environ['FLASK_ENV'] = 'development'
    app.run('0.0.0.0', debug=True)
