import os
import sqlite3
import importlib

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
    db = getattr(g, '_database', None) if g else None
    if db is None:
        db = sqlite3.connect(DB_PATH)
        if g:
            g._database = db
    db.row_factory = sqlite3.Row
    return db


def init():
    versions = schema_versions()
    current_version = version()
    version_max = max(versions)

    if current_version >= version_max:
        return

    print(
        f"Current database version is {current_version}, {version_max}" +\
        " available, performing database migrations."
    )
    while (version() < version_max):
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
    return sorted(q['name'].splitlines()) if q else []


def version():
    return execute("PRAGMA user_version", fetchone=True)['user_version']


def upgrade():
    set_schema(version() + 1)


def downgrade():
    set_schema(version() - 1)


def set_schema(ver):

    current = version()
    versions = schema_versions()

    upgrade = ver > current
    print(f"Preparing to do a schema {'upgrade' if upgrade else 'downgrade'}.")

    if ver == current:
        print("Already at version {current}, aborting.")
        return

    migration_version = ver if upgrade else current

    if migration_version not in versions:
        print(f"Version {migration_version} not available, aborting.")
        return

    migration = import_migration(migration_version)
    try:
        print(
            f"{'Up' if upgrade else 'Down'}grading database schema from" +\
            f" {current} -> {ver}"
        )
        migration.upgrade() if upgrade else migration.downgrade()
        set_version(ver)
    except:
        set_version(current)
        raise


def import_migration(version):

    versions = schema_versions()
    if version not in versions:
        err = f"Cannot upgrade to version: {version}, no such version"
        raise RuntimeError(err)

    spec = importlib.util.spec_from_file_location(
        "migration",
        versions[version]
    )
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    return migration


def set_version(version):
    get().execute(f"PRAGMA user_version = {version}")


def ip_to_int(ip_string):
    value = 0
    for p, num in enumerate(reversed(ip_string.split('.'))):
        value += pow(256, p)*int(num)
    return value


def int_to_ip(ip_as_int):
    tokens = []
    num_tokens = 4
    for exponent in reversed(range(num_tokens)):
        exp = pow(256, exponent)
        tokens.append(int(ip_as_int / exp))
        ip_as_int -= tokens[-1] * exp
    return '.'.join([str(t) for t in tokens])


def log_visit(endpoint, ip, method):
    execute(
        "INSERT INTO visit (endpoint, ip, method) VALUES (?,?,?);",
        (endpoint, ip_to_int(ip), method)
    )
    commit()


def visits():
    visits = []
    for visit in execute("SELECT * FROM visit;"):
        visits.append(dict(visit))
        visits[-1]['ip'] = int_to_ip(visits[-1]['ip'])
    return visits
