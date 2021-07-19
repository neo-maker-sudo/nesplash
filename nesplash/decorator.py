from flask import session, abort, redirect, url_for
from functools import wraps
from nesplash.models import User

def login_required(func):
    wraps(func)
    def wrapper_func(*args, **kwargs):
        if session.get("email") == None:
            abort(403)
        else:
            kwargs["email"] = session.get("email")
        return func(*args, **kwargs)
    wrapper_func.__name__ = func.__name__
    return wrapper_func


def admin_required(permission_name):
    def admin_decorate(func):
        wraps(func)
        def admin_wrapper_func(*args, **kwargs):
            sess = session.get("email")
            user = User.query.filter_by(email=sess).first()
            if not user.can(permission_name):
                abort(403)
            return func(*args, **kwargs)
        admin_wrapper_func.__name__ = func.__name__
        return admin_wrapper_func
    return admin_decorate
