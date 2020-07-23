#! /usr/bin/env python
# -*- coding: utf-8 -*-
from ihome.tasks.main import celery_app
from ihome.libs.yuntongxun.sms import CCP

@celery_app.task
def send_sms(to, datas, temp_id):
    """
    发送短信验证码的异步任务
    :return:celery -A ihome.tasks.main worker -l info
    """
    ccp = CCP()
    ccp.sendTemplateSMS(to, datas, temp_id)