# -*- coding:utf-8 -*-
from flask import Blueprint

# 创建一个蓝图
app_cart=Blueprint("app_cart", __name__,template_folder="templates")
# 在蓝图中需要指定模板目录 静态文件目录 但是当主目录与蓝图目录里都有对应的文件时，工程主目录的优先级最高

# 在  __init__文件被执行的时候 把视图加载进来  让蓝图与应用程程序知道视图的存在
from .views import get_cart
