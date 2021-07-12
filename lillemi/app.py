import os
from flask import render_template, Flask, redirect, url_for, request

from lillemi import db
from pathlib import Path
from secrets import token_hex

PATH_SECRET = Path(db.PATH_ROOT) / 'secret.txt'
if not PATH_SECRET.is_file():
    PATH_SECRET.write_text(token_hex(32))

app = Flask(__name__)
app.secret_key = PATH_SECRET.read_text()
app.config.update(
  SESSION_COOKIE_SECURE=True,
  SESSION_COOKIE_HTTPONLY=True,
  SESSION_COOKIE_SAMESITE='Lax',
)

with app.app_context():
    from lillemi import commands


@app.after_request
def after_request(response):

  def path_should_be_ignored():
    ignored_paths = ['/favicon', '/static/']
    if any([request.full_path.startswith(p) for p in ignored_paths]):
      return True
    return False

  if not path_should_be_ignored():
    db.log_visit(request.full_path, request.remote_addr, request.method)
  return response


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
    return render_template(
      'info.html',
      db_version=db.version(),
      schema_versions=db.schema_versions(),
      tables=db.tables(),
    )


@app.route('/info/traffic')
def traffic():
  return render_template('traffic.html', visits=db.visits())


def run():
    os.environ['FLASK_ENV'] = 'development'
    db.init()
    app.run('0.0.0.0', debug=True)
