import sqlite3
import base64
import Crypto.Util.number as cun
from . import id_gen


def select_id_gen(c):
    s = "SELECT p, g, e FROM id_gen;"
    c.execute(s)
    ans = c.fetchone()
    p = int(ans["p"])
    g = int(ans["g"])
    e = int(ans["e"])
    return (p, g, e)


def update_e(db, c, e):
    s = "UPDATE id_gen SET e = ?"
    c.execute(s, (str(e),))
    db.commit()


def insert_paste_with_id(db, c, id, body):
    s = "INSERT INTO paste (id, body) VALUES (?, ?)"
    c.execute(
        s,
        (
            str(id),
            body,
        ),
    )
    db.commit()


def insert_paste(db, body):
    c = db.cursor()
    p, g, e = select_id_gen(c)

    id = id_gen.gen_id(p, g, e)
    e += 1
    update_e(db, c, e)

    insert_paste_with_id(db, c, id, body)
    return id


def select_paste(c, id):
    s = "SELECT body FROM paste WHERE id = ?"
    c.execute(s, (id,))
    ans = c.fetchone()
    return ans["body"] if ans else None
