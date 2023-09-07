from flask import Blueprint, abort, request, redirect, url_for, flash, render_template
from flask_limiter import Limiter

from . import util
from .db import get_db
from .limiter import limiter

bp = Blueprint("paste", __name__)


@bp.route("/p/<int:paste_id>")
def get(paste_id):
    db = get_db()
    body = util.select_paste(db.cursor(), str(paste_id))
    if body:
        return render_template("paste/get.html", body=body)
    else:
        abort(404)


@bp.route("/", methods=("GET", "POST"))
@limiter.limit("20/minute", per_method=True, methods=["POST"])
def create():
    if request.method == "POST":
        error = None
        body = request.form.get("body")

        if not body:
            error = "You need to actually type something"
        elif len(body) > 256:
            error = "Exceeded 256 char limit"

        if not error:
            id = util.insert_paste(get_db(), body)
            return redirect(url_for("paste.get", paste_id=id))

        flash(error)

    return render_template("paste/create.html")
