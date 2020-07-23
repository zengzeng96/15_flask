#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-05 10:00:49

# here import the lib
from flask import Flask,current_app,redirect,url_for

app=Flask(__name__)

@app.route("/")
def index():
    return "Hello flask"


#通过methods限定访问方式
@app.route("/post_only",methods=["GET","POST"])
def post_only():
    return "post only page"

@app.route("/hello",methods=["POST"])
def hello():
    return "hello 1"

@app.route("/hello",methods=["GET"])
def hello2():
    return "hello 2"


@app.route("/hi1")
@app.route("/hi2")
def hi():
    return "hi page"
#两个动态地址访问同一个url

app.route("/login")
def login():
    # url="/"
    url=url_for("index")#反向解析  直接传入对应的视图函数的名字
    return redirect(url)
    
if __name__ == "__main__":
    # 查看整个flask中的路由信息
    print(app.url_map)
    # 启动flask程序
    app.run(debug=True)