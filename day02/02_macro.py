#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-11 10:29:07



# here import the lib
import sys
import os
import re
from flask import Flask,render_template,flash
app=Flask(__name__)

app.config["SECRET_KEY"]="SDCHDD"
flag=True
@app.route("/index")
def index():
    if flag:
        # 添加闪现信息
        flash("hello1")
        flash("hello2")
        flash("hello3")
        global flag
        flag=False
    return render_template("index.html")

def main():
    app.run(debug=True,port=8000)


if __name__ == "__main__":
    main()
    # pip install flask-mysqldb