import sqlite3
from datetime import datetime

import click
from flask import current_app, g


def getDB():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES

        )
        g.db.row_factory = sqlite3.Row

    return g.db


def closeDB(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def initDB():
    db = getDB()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def initDBCommand():
#Clear the existing data and create new tables.
    initDB()
    click.echo('Initialized database.')


sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromtimestamp(v.decode())

)    


def initApp(app):
    app.teardown_appcontext(closeDB)
    app.cli.add_command(initDBCommand)