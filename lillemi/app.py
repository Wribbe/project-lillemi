import os
from flask import render_template, Flask, redirect, url_for

from lillemi import db
from pathlib import Path
from secrets import token_hex

PATH_SECRET = Path(db.PATH_ROOT) / 'secret.txt'
if not PATH_SECRET.is_file():
    PATH_SECRET.write_text(token_hex(32))

app = Flask(__name__)
app.secret_key = PATH_SECRET.read_text()

with app.app_context():
    db.init()


@app.route('/')
def index():
    return redirect(url_for('born_yet'))


@app.route('/isshebornyet')
def born_yet():
    return render_template('born_yet.html', born=False)


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/info')
def info():
    return f"db version: {db.version()}"


def run():
    os.environ['FLASK_ENV'] = 'development'
    app.run('0.0.0.0', debug=True)
