from flask import render_template

from app import app


@app.errorhandler(400)
def bad_request(error):
    return render_template("errors/400.html"), 400


@app.errorhandler(401)
def page_not_found(error):
    return render_template("errors/401.html"), 401


@app.errorhandler(404)
def server_error(error):
    return render_template("errors/404.html"), 404
