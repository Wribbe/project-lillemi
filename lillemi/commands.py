import click

from lillemi import db
from flask import current_app as app
from flask.cli import AppGroup


groups = g = {
    'database': AppGroup(
        'database',
        short_help="Commands related to the database"
    ),
}


@g['database'].command("upgrade")
def upgrade():
    """Set database schema to a newer version if it exists"""
    db.upgrade()


@g['database'].command("downgrade")
def downgrade():
    """Set database schema to previous version if such exists"""
    db.downgrade()


for group in groups.values():
    app.cli.add_command(group)
