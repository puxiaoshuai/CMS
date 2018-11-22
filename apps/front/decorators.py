from functools import wraps
from flask import g, redirect, session, url_for
import config


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get(config.FRONT_USER_ID):
            return wrapper(*args, **kwargs)
        else:
            return redirect(url_for('front.sign_in'))
    return wrapper
