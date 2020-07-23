# -*- coding:utf-8 -*-
from werkzeug.routing import BaseConverter
from flask import session, jsonify, g
from ihome.utils.response_code import RET
import functools


# 定义正则转换器
class ReConverter(BaseConverter):
    """

    """

    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super(ReConverter, self).__init__(url_map)
        self.regex = regex


# 自定义的验证登录状态的装饰器
def login_required(view_func):
    @functools.wraps(view_func)
    def wrapper(*args, **kwargs):  # 上面的是保存view函数的元属性
        # 判断用户的登录状态
        # 登录  执行视图函数
        user_id = session.get("user_id")
        if user_id is not None:
            # 将user_id保存到g对象中，在视图函数中可以通过g对象获取保存的数据
            g.user_id = user_id
            return view_func(*args, **kwargs)
        # 如果未登录  返回未登录信息
        else:
            return jsonify(errno=RET.SESSIONERR, errmsg="用户未登录")

    return wrapper


# @login_required
# def set_user_avatar():
#     user_id = g.user_id
#     return jsonify
