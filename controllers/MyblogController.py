# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/29
@updated: 2017/03/29
"""

from flask import Blueprint, request, url_for, redirect, current_app,\
 render_template, abort, g
# import flask.ext.sqlalchemy
from application import db
from models.paper import Paper
from models.user import User
from common.functions import auth

myblog_bp = Blueprint('myblog', __name__, url_prefix='/myblog')


@myblog_bp.route('', methods=['GET'])
@auth
def myblog():
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
    # s = '的博客'.decode('utf-8')
    # print type(s)
    username = username+u'的博客'
    return render_template('mainpage.html', papers=papers, pagination=pagination, \
        username=username, type='myblog')

@myblog_bp.route('/delete', methods=['GET'])
@auth
def myblog_delete():
    paperid = request.args.get('paperid', None)
    if paperid is not None:
        paper_existd = Paper.query.filter_by(p_id=paperid).first()
        if paper_existd is not None:
            if paper_existd.u_id == getattr(g, 'u_id'):
                paper_existd.delete()
            else:
                abort(403)
    abort(400)




