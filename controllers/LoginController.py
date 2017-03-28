# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/26
@updated: 2017/03/26
"""

from flask import Blueprint, request, session, url_for, redirect, render_template,\
                make_response, g
from common.functions import convert_password
from models.user import User
from models.session import Session

import json
import uuid
import time
import unicodedata
import re

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('', methods=['GET', 'POST'])
def login():
    """
    handle users' login
    """
    if request.method == 'GET':
        return render_template('login.html', error='', type='login')

    try:
        username, password = request.form['username'], request.form['password']

    except Exception as e:
        print e

        return render_template('login.html', error=u'请求参数错误'), 400

    session.permanent = True

    session_id = request.cookies.get('session_id')

    if session_id is not None:
        session_existed = Session.query.filter_by(session_id=session_id).first()

        if session_existed is not None:
            if int(session_existed.expires > time.time()):
                data = eval(session_existed.data)

                res = make_response(redirect(url_for('mainpage.mainpage')))
                res.set_cookie('session_id', str(data['id']), expires=session_existed.expires)
                return res
            else:
                Session().delete(session_id=session_id)

    user_existed = User.query.filter_by(username=username).first()
    if user_existed is None:
        return render_template('login.html', error=u'用户不存在', type='login')
    if user_existed.password != convert_password(password):
        return render_template('login.html', error=u'密码错误', type='login')


    new_session_id = uuid.uuid4()

    resp_data = {
    'id' : user_existed.u_id,
    'username': user_existed.username.encode('ascii')
    }

    cookie_expires = int(time.time())+10800

    Session().create(
        session_id=str(new_session_id),
        expires=cookie_expires,
        data=str(resp_data)
    )

    res = make_response(redirect(url_for('mainpage.mainpage')))
    res.set_cookie('session_id', str(new_session_id), expires=cookie_expires)

    return res












