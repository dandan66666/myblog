# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/26
@updated: 2017/03/26
"""

from application import db

class Comment(db.Model):

    __table__ = db.Table('comment', db.metadata,
        db.Column('c_id', db.BigInteger, primary_key=True, autoincrement=True),
        db.Column('u_id', db.BigInteger, db.ForeignKey('user.u_id'), nullable=False),
        db.Column('p_id', db.BigInteger, db.ForeignKey('paper.p_id'), nullable=False),
        db.Column('content', db.VARCHAR(200), nullable=False),
        mysql_engine='InnoDB',
        mysql_charset='utf8'

        )

    def save(self):
        db.session.add(self)
        db.session.commit()


    def __repr__(self):
        return '<Comment %r>' % self.c_id