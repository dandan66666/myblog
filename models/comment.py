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
        db.Column('created_at', db.DateTime, default=db.text("CURRENT_TIMESTAMP")),
        db.Column('updated_at', db.DateTime, default=db.text("CURRENT_TIMESTAMP")),
        mysql_engine='InnoDB',
        mysql_charset='utf8'

        )

    def save(self):
        db.session.add(self)
        db.session.commit()

    def create(self, u_id, p_id, content, created_at=None, updated_at=None):
        self.u_id = u_id
        self.p_id = p_id
        self.content = content
        if created_at is not None:
            self.created_at = created_at
        if updated_at is not None:
            self.updated_at = updated_at
        self.save()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


    def __repr__(self):
        return '<Comment %r>' % self.c_id