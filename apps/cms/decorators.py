from functools import wraps
from flask import session, url_for, redirect
import config


def login_requied(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get(config.CMS_USER_ID):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))

    return wrapper
