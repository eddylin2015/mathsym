from flask import current_app, Flask, redirect, request, render_template,send_file,\
     session,url_for,Blueprint
import model_cloudsql as model
from functools import wraps

def login_required_auth(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('profile') is None:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function       


def get_model():
    #model = model_cloudsql
    return model
