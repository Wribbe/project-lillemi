import os
import sqlite3

from flask import g, current_app
from pathlib import Path

FORMAT_DB_SCHEMA = "{:04d}_schema.sql"
PATH_ROOT = Path(__file__).parent.parent
PATH_SCHEMAS = PATH_ROOT / 'lillemi' / 'schemas'
PATH_DATA = Path(os.environ.get('LILLEMI_PATH_DATA', PATH_ROOT))

if not PATH_DATA.is_dir():
    PATH_DATA.mkdir()

PATH_DB = PATH_DATA / 'lillemi.sqlite3'


def get():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(PATH_DB)
    db.row_factory = sqlite3.Row
    return db


def init():
    if PATH_DB.is_file():
        return
    print("Initializing database.")
    db = get()
    with current_app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


def execute(query, vals=None, fetchone=False):
    q = get().cursor().execute(query, vals if vals else ())
    return q.fetchone() if fetchone else q.fetchall()


def commit():
    get().commit()


def schemas():
    schemas = {}
    for file in  sorted(PATH_SCHEMAS.iterdir()):
        if not file.suffix == ".sql":
            continue
        version = int(file.stem.split('_')[0])
        schemas[version] = file
    return schemas


def version():
    return execute("PRAGMA user_version", fetchone=True)['user_version']
