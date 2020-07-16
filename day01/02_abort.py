#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-07 10:54:26
# @Author  : ZENG JIA (zengjia42@126.com)
# @Link    : https://weibo.com/5504445825/profile?topnav=1&wvr=6


# here import the lib
from flask import Flask, request, abort, Response

app = Flask(__name__)


@app.route("/login", methods=["GET"])
def login():
    """接受前端传送过来的文件
    @return:
    """
    # name = request.form.get("name")
    # pwd = request.form.get("age")
    name = ""
    pwd = ""
    if name != "zhangsan" or pwd != "admin":
        # 使用 abort 函数可以立即终止视图函数的执行   并且可以返回前端特定的信息
        # 1.传递状态码信息
        abort(404)  # 必须是标准的状态码   不能传入 666  等
        # 2.传递响应信息
        # resp = Response("login failed")
        # abort(resp)

    return "login sucess"


# 定义错误的处理方法
@app.errorhandler(404)
def hand_404_erro(err):
    """自定义404状态码的错误函数"""
    # 这个函数的返回值会是前端用户最终看到的结果
    return u'出现了404错误 错误信息：%s'%err



def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
