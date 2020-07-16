#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-07 11:12:55
# @Author  : ZENG JIA (zengjia42@126.com)
# @Link    : https://weibo.com/5504445825/profile?topnav=1&wvr=6


# here import the lib
import sys
import os
import re
from flask import Flask, request, Response,make_response

app = Flask(__name__)


@app.route("/index")
def index():
    """
    处理返回信息
    @return:
    """
    # 1.使用元组 返回自定义的响应信息
    #               响应体       状态码 响应头
    # return "index page",400,[("zengjia","python"),("city","beijing")]
    # return "index page", 400, {"itcast": "python", "city": "beijing"}
    # return "index page", "666 itcast status ok", {"itcast": "python", "city": "beijing"}
    # return "index page", "666 itcast status ok"#可以不传后面的响应头
    # 666 itcast status ok  指明响应代码的说明信息
    '''
    Content-Length: 10
    Content-Type: text/html; charset=utf-8
    Date: Sat, 07 Mar 2020 03:15:22 GMT
    Server: Werkzeug/1.0.0 Python/2.7.16
    '''
    # 2.使用make_response 来构造响应信息
    resp=make_response("index page 2")#响应体信息
    resp.status="999 itcast"#设置状态码
    resp.headers["city"]="shanghai"#设置响应头
    return resp

# 返回json信息
def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
