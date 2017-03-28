from flask_wtf import Form
from wtforms import SubmitField, StringField
from wtforms.validators import Required
from flask_pagedown.fields import PageDownField
from flask import Blueprint, request, render_template, session, g
from markdown import markdown
import bleach

from common.functions import auth
from models.session import Session
from models.paper import Paper

writepaper_bp = Blueprint('writepaper', __name__, url_prefix='/writepaper')

allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code',
                'em', 'i', 'img', 'li', 'ol', 'pre', 'strong', 'ul', 'h1',
                 'h2', 'h3', 'p' ]

fp_path = 'static/papers/'

class PostForm(Form):
    title = StringField(u'Title')
    pagedown = PageDownField("What's on your mind?", validators=[Required()])
    submit = SubmitField('Submit')

@writepaper_bp.route('', methods=['GET', 'POST'])
@auth
def writepaper():
    if request.method == 'GET':
        form = PostForm()
        return render_template('writepaper.html', form=form)
    data = request.form['pagedown']
    md = markdown(data, out_format='html')
    html = bleach.linkify(bleach.clean(md, tags=allowed_tags, strip=True))
    
    userid = getattr(g, 'u_id')
    last = Paper.query.order_by(Paper.p_id.desc()).first()
    if last is None:
        paperid = 1
    else:
        paperid = last.p_id+1
    title = request.form['title']

    print g.__dict__
    print userid

    Paper().create(userid, title, fp_path+str(paperid))
    with open(fp_path+str(paperid)+'_html.txt', 'w') as fp:
        fp.write(html)
    with open(fp_path+str(paperid)+'_md.txt', 'w') as fp:
        fp.write(data)

    return render_template('readpaper.html', content=html)






