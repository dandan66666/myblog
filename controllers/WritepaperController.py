# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/28
@updated: 2017/03/28
"""

from flask_wtf import Form
from flask import Blueprint, request, render_template, session, g, redirect, \
                    url_for, abort
from markdown import markdown
import bleach

from common.functions import auth
from models.session import Session
from models.paper import Paper

writepaper_bp = Blueprint('writepaper', __name__, url_prefix='/writepaper')

allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'br', 'code',
                'em', 'i', 'img', 'li', 'ol', 'pre', 'strong', 'ul', 'h1',
                 'h2', 'h3', 'p', 'span', 'table', 'th', 'td', 'tr']

fp_path = 'static/papers/'

@writepaper_bp.route('', methods=['GET', 'POST'])
@auth
def writepaper():
    if request.method == 'GET':
        paperid = request.args.get('paperid', None)

        if paperid is not None:
            paper_existed = Paper.query.filter_by(p_id=paperid).first()

            # 不是本人写的博客不能修改
            if paper_existed.u_id != getattr(g, 'u_id'):
                abort(403)
            
            if paper_existed is not None:
                content = ''
                with open(paper_existed.path+'_md.txt', 'r') as fp:
                    content = fp.read()

                print paper_existed.title
                return render_template('writepaper.html', title=paper_existed.title, \
                    content=content.decode('utf-8'), id=paper_existed.p_id)

        return render_template('writepaper.html', title='', content='', id=0)
    
    data = request.form['content']
    md = markdown(data, out_format='html', extensions=['markdown.extensions.tables', 
        'markdown.extensions.codehilite', 'markdown.extensions.fenced_code'])
    print md
    html = bleach.linkify(bleach.clean(md, tags=allowed_tags, strip=True))
    
    
    paperid = request.form['id']
    title = request.form['title']

    print 'paperid', paperid
    print 'type ', type(md)

    # 创建一篇新的文章
    if int(paperid) == 0:
        last = Paper.query.order_by(Paper.p_id.desc()).first()
        # print 'last', last
        if last is None:
            paperid = 1
            print 'None', paperid
        else:
            paperid = last.p_id+1
            print last.p_id, paperid

        userid = getattr(g, 'u_id')
        Paper().create(userid, title, fp_path+str(paperid))
    # 修改已有的文章
    else:
        paper_existed = Paper.query.filter_by(p_id=paperid).first()
        if paper_existed is not None:
            paper_existed.title = title
            paper_existed.save()
        
    print paperid

    with open(fp_path+str(paperid)+'_html.txt', 'w') as fp:
        fp.write(html.encode('utf-8'))
    with open(fp_path+str(paperid)+'_md.txt', 'w') as fp:
        fp.write(data.encode('utf-8'))

    return redirect(url_for('mainpage.mainpage'))






