# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/26
@updated: 2017/03/26
"""

from application import db

class Paper(db.Model):

    __table__ = db.Table('paper', db.metadata,
        db.Column('p_id', db.BigInteger, primary_key=True, autoincrement=True),
        db.Column('u_id', db.BigInteger, db.ForeignKey('user.u_id'), nullable=False),
        db.Column('title', db.VARCHAR(128), nullable=False),
        db.Column('path', db.VARCHAR(128), nullable=False),
        db.Column('created_at', db.DateTime, default=db.text("CURRENT_TIMESTAMP")),
        db.Column('updated_at', db.DateTime, default=db.text("CURRENT_TIMESTAMP")),
        mysql_engine='InnoDB',
        mysql_charset='utf8'
        )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self, u_id, title, path):
        self.u_id = u_id
        self.title = title
        self.path = path
        self.save()

    def delete(self):
        db.session.delete(self)
        db.sesssion.commit()

    def __repr__(self):
        return '<Paper %r>' % self.title