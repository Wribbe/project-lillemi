import os
from flask import render_template, Flask, redirect, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return redirect(url_for('born_yet'))


@app.route('/isshebornyet')
def born_yet():
    return render_template('born_yet.html', born=False)


@app.route('/login')
def login():
    return render_template('login.html')


def run():
    os.environ['FLASK_ENV'] = 'development'
    app.run('0.0.0.0', debug=True)
