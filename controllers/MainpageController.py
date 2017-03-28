# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/26
@updated: 2017/03/26
"""

from flask import Blueprint, request, url_for, redirect, current_app,\
 render_template, abort, g
# import flask.ext.sqlalchemy
from application import db
from models.paper import Paper
from models.user import User
from common.functions import auth

mainpage_bp = Blueprint('mainpage', __name__, url_prefix='/mainpage')


@mainpage_bp.route('', methods=['GET'])
@auth
def mainpage():
    userid = getattr(g, 'u_id')
    username = getattr(g, 'username')
    if userid is None:
        abort(400)
    page = request.args.get('page', 1, type=int)
    pagination = Paper.query.filter_by(u_id=userid).order_by(Paper.updated_at.desc()).paginate(
        page, per_page=current_app.config['FLASKY_POSTS_PER_PSGE'],
        error_out=False
        )
    papers = pagination.items
    return render_template('mainpage.html', papers=papers, pagination=pagination, \
        username=username)
