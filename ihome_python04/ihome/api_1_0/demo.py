# coding:utf-8
from . import api
from ihome import db, models
from flask import current_app


@api.route("/index")
def index():
    current_app.logger.error('erro message')
    current_app.logger.warn('warn message')
    current_app.logger.info('info message')
    current_app.logger.debug('debug message')
    return 'index page'
