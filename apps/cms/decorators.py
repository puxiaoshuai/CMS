from functools import wraps
from flask import session, url_for, redirect, g
import config


def login_requied(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get(config.CMS_USER_ID):
            return func(*args, **kwargs)
        else:
            return redirect(url_for('cms.login'))

    return wrapper


def permission_requied(permission):
    def outter(func):
        @wraps(func)
        def inner(*args, **kwargs):
            user = g.cms_user
            if user.has_perssion(permission):
                return func(*args, **kwargs)
            else:
                return redirect(url_for('cms.index'))

        return inner

    return outter
