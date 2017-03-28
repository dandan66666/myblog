# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/26
@updated: 2017/03/26
"""
from application import db

class User(db.Model):

    __table__ = db.Table('user', db.Model.metadata,
        db.Column('u_id', db.BigInteger, primary_key=True, autoincrement=True),
        db.Column('username', db.VARCHAR(64), nullable=False),
        db.Column('password', db.VARCHAR(64), nullable=False),
        db.Column('created_at', db.DateTime, default=db.text("CURRENT_TIMESTAMP")),
        db.Column('updated_at', db.DateTime, default=db.text("CURRENT_TIMESTAMP")),
        mysql_engine='InnoDB',
        mysql_charset='utf-8'

        )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self, username, password):
        self.username = username
        self.password = password
        self.save()

    def __repr__(self):
        return '<User %r>' % self.username
