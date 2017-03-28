# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/26
@updated: 2017/03/26
"""
from application import db

class Session(db.Model):

    __table__ = db.Table('session', db.metadata,
        db.Column('session_id', db.VARCHAR(128), primary_key=True),
        db.Column('expires', db.Integer, nullable=False),
        db.Column('data', db.JSON),
        mysql_engine='InnoDB',
        mysql_charset='utf-8'
        )

    def save(self):
        db.session.add(self)
        db.session.commit()


    def create(self, session_id, expires, data):
        self.session_id = session_id
        self.expires = expires
        self.data = data
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return '<Session %r>' % self.session_id