# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/26
@updated: 2017/03/26
"""

from flask import Blueprint, request, session, redirect, url_for
from models.session import Session

logout_bp = Blueprint('logout', __name__, url_prefix='/logout')

@logout_bp.route('', methods=['GET'])
def logout():
    session_id = request.cookies.get('session_id')

    session_existed = Session.query.filter_by(session_id=session_id).first()

    # session['u_id'] = None

    if session_existed is not None:
        session_existed.delete()
    
    return redirect(url_for('login.login'))