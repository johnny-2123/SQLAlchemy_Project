from app import flask_app as app
from app.models import Pony
from flask import render_template


@app.route("/")
@app.route("/index")
def index():
    pony_count = Pony.query.count()
    return render_template("index.html", pony_count=pony_count)
