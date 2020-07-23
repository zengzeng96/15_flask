# -*- coding:utf-8 -*-
from flask import Blueprint

# 创建一个蓝图
app_cart = Blueprint("app_cart", __name__, template_folder="templates")#这个模版目录会优先渲染工程目录下的templates目录下的html文件

# 在蓝图中需要指定模板目录 静态文件目录 但是当主目录与蓝图目录里都有对应的文件时，工程主目录的优先级最高
# 也就是说上面的templates_folder是必须写的
# 不然的话就添加不进去

# 在  __init__文件被执行的时候 把视图加载进来  让蓝图与应用程程序知道视图的存在
from .views import get_cart
