# coding: utf-8

"""
@description: web server of blog
@author: Shijuan Lu<243050994@qq.com>
@created: 2017/03/26
@updated: 2017/03/26
"""

import logging
import logging.handlers

logging.basicConfig(
    level = logging.INFO,
    format = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
    datefmt = '%Y-%m-%d %H:%M:%S'
)

console_handler = logging.StreamHandler()

class BlogConfig(object):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:matrix123456@localhost/blog'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

