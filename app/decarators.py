from functools import wraps
from flask import session, flash, redirect, url_for


def login_required(required=True):
    def decorator(func):
        @wraps(func)
        def inner_decorator(*args, **kwargs):
            if required and not session.get("user_id"):
                flash("First you need loged in", "danger")
                return redirect(url_for("login"))
            if not required and session.get("user_id"):
                flash("You are already loged in", "info")
                return redirect(url_for("home"))

            return func(*args, **kwargs)

        return inner_decorator
    return decorator
