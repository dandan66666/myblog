# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/28
@updated: 2017/03/28
"""

from flask import Blueprint, request, g, abort, render_template
from common.functions import auth
from models.paper import Paper
from controllers.ManagecommentController import get_comments

readpaper_bp = Blueprint('readpaper', __name__, url_prefix='/readpaper')

@readpaper_bp.route('', methods=['GET'])
@auth
def showpaper():
    paperid = request.args.get('paperid', None)
    if paperid is not None:
        print paperid
        paper_existd = Paper.query.filter_by(p_id=paperid).first()
        path = paper_existd.path
        title = paper_existd.title

        userid = paper_existd.u_id
        modified = False

        if getattr(g, 'u_id') == userid:
            modified = True
        print 'readtype', type(title)
        print title.encode('utf-8')
        with open(path+'_html.txt', 'r') as fp:
            html = fp.read()
        html = '<h1>'+title.encode('utf-8')+'</h1>'+html

        comments = get_comments(paperid)

        return render_template('readpaper.html', content=html.decode('utf-8'), \
            paperid=paper_existd.p_id, modified=modified, comments=comments)
    abort(400)


@readpaper_bp.route('/delete/<int:paperid>', methods=['GET'])
@auth
def deletepaper(paperid):
    paperid = request.args.get('paperid', None)
    if paperid is not None:
        paper_existd = Paper.query.filter_by(p_id=paperid).first()
        if paper_existd is not None:
            if paper_existd.u_id == getattr(g, 'u_id'):
                paper_existd.delete()
                return redirect(url_for('myblog.myblog'))
            else:
                abort(403)
    abort(400)
        




