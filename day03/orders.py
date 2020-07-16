# -*- coding:utf-8 -*-
from flask import Blueprint

# 创建一个蓝图对象   就是一个小模块的抽象的概念
app_orders=Blueprint("app_orders", __name__)

@app_orders.route("/get_orders")
def get_orders():
    return "get_order page"


@app_orders.route("/post_orders")
def post_orders():
    return "post_order page"