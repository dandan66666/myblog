# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/26
@updated: 2017/03/26
"""
from flask import Flask, Blueprint

import os
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_pagedown import PageDown
from config import BlogConfig


app = Flask(__name__)

app.config.from_object('config.BlogConfig')

app.config['FLASKY_POSTS_PER_PSGE'] = 20

db = SQLAlchemy(app)

bootstrap = Bootstrap(app)

pagedown = PageDown(app)

# session_id
app.secret_key = os.urandom(24)
app.permanent_session_lifetime = timedelta(minutes=180)


from controllers.LoginController import login_bp
app.register_blueprint(login_bp)

from controllers.SignupController import signup_bp
app.register_blueprint(signup_bp)

from controllers.LogoutController import logout_bp
app.register_blueprint(logout_bp)

from controllers.MainpageController import mainpage_bp
app.register_blueprint(mainpage_bp)

from controllers.WritepaperController import writepaper_bp
app.register_blueprint(writepaper_bp)



