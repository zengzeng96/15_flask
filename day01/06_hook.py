#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-07 22:07:29
# @Author  : ZENG JIA (zengjia42@126.com)
# @Link    : https://weibo.com/5504445825/profile?topnav=1&wvr=6


# here import the lib
from flask import Flask, request

app = Flask(__name__)


@app.route("/hello")
def hello():
    print("hello 被执行")
    return "hello page"


@app.route("/index")
def index():
    print("index 被执行")
    # 设置一个异常
    # a = 1 / 0
    return "index page"


@app.before_first_request
def handle_before_first_request():
    """在第一次请求之前被执行"""
    print("handle_before_first_request 被执行")


@app.before_request
def handle_before_request():
    """在每次请求之前都会被执行"""
    print("handle_before_request 被执行")


@app.after_request
def handle_after_request(response):
    """在每次请求（视图函数）之后都会被执行  视图函数没有出现异常"""
    print("handle_after_request 被执行")
    return response


@app.teardown_request
def handle_teardown_request(response):
    """在每次请求之后   视图函数处理之后 都会被执行  无论视图函数是否出现异常都被执行"""
    print("handle_teardown_request 被执行   工作在非调试模式下  debuig=False")
    print(request.path)
    return response


def main():
    # app.run(debug=True)
    app.run()


if __name__ == "__main__":
    main()
