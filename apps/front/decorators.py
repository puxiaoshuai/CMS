from functools import wraps
from flask import g, redirect, session, url_for
import config


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if config.FRONT_USER_ID in session:
            return func(*args, **kwargs)
        else:
            return redirect(url_for('front.sign_in'))
    return wrapper
