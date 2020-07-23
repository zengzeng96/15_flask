#! /usr/bin/env python
# -*- coding: utf-8 -*-

from celery import Celery
from ihome.tasks import config

# 定义Celery对象
celery_app = Celery("ihome")
# 引入配置信息
celery_app.config_from_object("ihome.tasks.config")
# 自动搜寻异步任务
celery_app.autodiscover_tasks(["ihome.tasks.sms"])
