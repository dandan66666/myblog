# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/26
@updated: 2017/03/26
"""

from flask import Blueprint, request, url_for, redirect, render_template, \
            make_response, g, session
from models.user import User
from models.session import Session
from common.functions import convert_password

import time
import uuid

signup_bp = Blueprint('signup', __name__, url_prefix='/signup')

@signup_bp.route('', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('login.html', error='', type='signup')
    else:
        try:
            username = request.form['username']
            password = request.form['password']
            confirm = request.form['confirm']

            


            username_existed = User.query.filter_by(username=username).first()

            if username_existed is not None:
                return render_template('login.html', error=u'用户名已存在', type='signup'), 400
            if len(username) > 64:
                return render_template('login.html', error=u'用户名超过64位', type='signup'), 400
            if password != confirm:
                return render_template('login.html', error=u'两次输入的密码不匹配', type='signup'), 400
            if len(password) > 64:
                return render_template('login.html', error=u'密码超过64位', type='signup'), 400

        except Exception as e:
            print e
            return render_template('login.html', error=u'请求参数错误'+str(e), type='signup'), 400

        User().create(username, convert_password(password))
        user_existed = User.query.filter_by(username=username).first()

        session_id = uuid.uuid4()
        resp_data = {
        'id': user_existed.u_id,
        'username': username
        }
        expires = int(time.time())+10800
        Session().create(session_id, expires, str(resp_data))

        res = make_response(redirect(url_for('mainpage.mainpage')),  200)
        res.set_cookie('session_id', str(session_id), expires=expires)
        return res

