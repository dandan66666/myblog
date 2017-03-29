# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/29
@updated: 2017/03/29
"""

from flask import Blueprint, request, g, url_for

from models.comment import Comment
from models.user import User
from common.functions import auth

managecomment_bp = Blueprint('managecomment', __name__, '/comment')

@managecomment_bp.route('/get', methods=['GET'])
@auth
def get_comment():
    paperid = request.args.get('paperid', None)
    if paperid is not None:
        comments = []
        comments_existed = Comment.query.filter_by(p_id=paperid).all()
        if comments_existed is not None:
            for comment_existed in comments_existed:
                comment={}
                comment['content'] = comment_existed.content;
                comment['id'] = comment_existed.c_id;
                author = User.query.filter_by(u_id=comment_existed.u_id).first()
                if author is not None:
                    comment['author'] = author.username
                else:
                    comment['author'] = None
                comments.append(comment)
        return comments
    abort(400)

@managecomment_bp.route('/add', methods=['POST'])
@auth
def add_comment():
    content = request.form
    if content is not None:
        paperid = content['paperid']
        userid = getattr(g, 'u_id')
        comment = content['content']
        Comment().create(userid, paperid, comment)
        return redirect(url_for('readpaper', paperid=paperid))
    abort(400)

@managecomment_bp.route('/update', methods=['POST'])
@auth
def update_comment():
    content = request.form
    if content is not None:
        commentid = content['id']
        comment = content['content']
        comment_existed = Comment.query.filter_by(c_id=commentid).first()
        if comment_existed is not None:
            comments_existed.comment = comment
            comment_existed.save()
            return redirect(url_for('readpaper', paperid=paperid))
    abort(400)

@managecomment_bp.route('/delete', methods=['GET'])
@auth
def delete_comment():
    commentid = request.args.get('commentid', None)
    if commentid is not None:
        comment_existed = Comment.query.filter_by(c_id=commentid).first()
        if comment_existed is not None:
            comment_existed.delete()
        else:
            abort(400)
    else:
        abort(400)



