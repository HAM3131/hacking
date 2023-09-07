import os
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

import Crypto.Random.random as crr
from . import id_gen
from . import util

from faker import Faker


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"], detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_id_gen(db):
    # Takes too long to generate a safe prime each time (like 4 seconds!! I'm
    # on a GODDAMN SCHEDULE HERE), so I'm just going to hardcode it.
    # p = id_gen.gen_safe_prime()
    p = 234146428696455141502482141719214063107

    # This number is SECRET!
    g = id_gen.gen_g(p)

    # This number is ALSO SECRET!
    e = id_gen.gen_e(p)

    c = db.cursor()
    s = "INSERT INTO id_gen (p, g, e) VALUES (?, ?, ?);"
    c.execute(
        s,
        (
            str(p),
            str(g),
            str(e),
        ),
    )
    db.commit()


def get_init_pastes():
    ans = [os.environ.get("FLAG")]
    Faker.seed(1234)
    fake = Faker()
    ans += [fake.sentence(nb_words=10) for _ in range(42)]
    ans += ["https://youtu.be/dQw4w9WgXcQ"]
    ans += [fake.sentence(nb_words=10) for _ in range(30)]
    return ans


def init_pastes(db):
    bodies = get_init_pastes()
    for body in bodies:
        util.insert_paste(db, body)


def init_db():
    db = get_db()

    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

    init_id_gen(db)
    init_pastes(db)


@click.command("init_db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
