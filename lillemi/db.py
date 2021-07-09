import os
import sqlite3

from flask import g, current_app
from pathlib import Path

DB_FORMAT_SCHEMA = "{:04d}.py"
PATH_ROOT = Path(__file__).parent.parent
PATH_SCHEMAS = PATH_ROOT / 'lillemi' / 'migrations'
PATH_DATA = Path(os.environ.get('LILLEMI_PATH_DATA', PATH_ROOT))

if not PATH_DATA.is_dir():
    PATH_DATA.mkdir()

DB_PATH = PATH_DATA / 'lillemi.sqlite3'
DB_CONN = None


def get():
    global DB_CONN
    db = getattr(g, '_database', None) if g else None
    if db is None:
        db = sqlite3.connect(DB_PATH)
        if g:
            g._database = db
        if not DB_CONN:
            DB_CONN = db
            init()
    db.row_factory = sqlite3.Row
    return db


def init():
    versions = schema_versions()
    current_version = version()
    verisons_max = max(versions)

    if current_version == verisons_max:
        print("No pending migrations available.")
        return

    print(
        f"Current database version is {current_version}, {verisons_max}" +\
        " available, performing database migrations."
    )
    while (version() < verisons_max):
        upgrade()


def execute(query, vals=None, fetchone=False):
    q = get().cursor().execute(query, vals if vals else ())
    return q.fetchone() if fetchone else q.fetchall()


def execute_one(*args, **kwargs):
    kwargs['fetchone'] = True
    return execute(*args, **kwargs)


def executescript(script):
    return get().cursor().executescript(script)


def commit():
    get().commit()


def schema_versions():
    schemas = []
    for file in  sorted(PATH_SCHEMAS.iterdir()):
        if not file.suffix == ".py":
            continue
        if not file.stem.isdigit():
            continue
        version = int(file.stem)
        schemas.append((version, file))
    return dict(sorted(schemas))


def tables():
    q = execute_one("SELECT name from sqlite_master WHERE type='table';")
    return sorted(q['name'].splitlines())


def version():
    return execute("PRAGMA user_version", fetchone=True)['user_version']


def upgrade():
    print("UPGRADE")


def downgrade():
    print("DOWNGRADE")
