# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/29
@updated: 2017/03/29
"""

from flask import Blueprint, request, g, url_for, make_response

from models.comment import Comment
from models.user import User
from common.functions import auth, convert_jstime_to_datetime

import json
from datetime import datetime

managecomment_bp = Blueprint('managecomment', __name__, url_prefix='/comment')

@managecomment_bp.route('/', methods=['GET'])
@auth
def show_comment():
    return "Hello world"

def get_comments(paperid):
    if paperid is not None:
        comments = []
        comments_existed = Comment.query.filter_by(p_id=paperid).all()
        if comments_existed is not None:
            for comment_existed in comments_existed:
                comment={}
                comment['content'] = comment_existed.content
                comment['id'] = comment_existed.c_id
                comment['time'] = comment_existed.updated_at
                author = User.query.filter_by(u_id=comment_existed.u_id).first()
                if author is not None:
                    comment['author'] = author.username
                else:
                    comment['author'] = None
                comments.append(comment)
        return comments
    return None

@managecomment_bp.route('/add', methods=['GET','POST'])
@auth
def add_comment():
    if request.method == 'GET':
        return None
    posted = request.get_json()
    if posted is not None:
        paperid = int(posted['paperid'])
        userid = getattr(g, 'u_id')
        time_ = posted['time']
        time_ = convert_jstime_to_datetime(time_)
        comment = posted['content']
        Comment().create(userid, paperid, comment, updated_at=time_)
        

        print comment
        
        user_existd = User.query.filter_by(u_id=userid).first()
        if user_existd is not None:
            username = user_existd.username
        else:
            username = ''

        comment_existed = Comment.query.order_by(Comment.c_id.desc()).first()
        if comment_existed is not None:
            commentid = comment_existed.c_id
        else:
            commentid = 0
        
        out = {
        'username': username,
        'commentid': commentid,
        'time': time_.strftime("%Y-%m-%d %H:%m:%S")
        }
        
        return json.dumps(out)
    return None

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
            return True
    return False

@managecomment_bp.route('/delete', methods=['GET'])
@auth
def delete_comment():
    commentid = request.args.get('commentid', None)
    if commentid is not None:
        comment_existed = Comment.query.filter_by(c_id=commentid).first()
        if comment_existed is not None and comment_existed.u_id == getattr(g, 'u_id'):
            comment_existed.delete()
            return True
    return False



