# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/26
@updated: 2017/03/26
"""
from flask import request, g, session, render_template, redirect, url_for
from functools import wraps
from models.session import Session
import hashlib
import time

def auth(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        session_id = str(request.cookies.get('session_id'))

        if session_id is not None:
            session_existed = Session.query.filter_by(session_id=session_id).first()

            if session_existed is not None and \
                session_existed.expires > int(time.time()):
                    data = eval(session_existed.data)
                    setattr(g, 'u_id', data['id'])
                    setattr(g, 'username', data['username'])
                    return func(*args, **kwargs)

        return redirect(url_for('login.login', error=True))

    return wrapper

def rowToDict(row):
    d = {}
    for column in row.__table__.columns:
        d[column.name] = getattr(row, column.name)
    return d

def convertSQLResultToList(sql_result):
    return [rowToDict(row) for row in sql_result]

def convert_password(password):
    return hashlib.sha1(password).hexdigest()





