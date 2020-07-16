#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-13 15:14:37
# @Author  : ZENG JIA (zengjia42@126.com)
# @Link    : https://weibo.com/5504445825/profile?topnav=1&wvr=6


# here import the lib
import sys
import os
import re

from flask import Flask,request,jsonify
app=Flask(__name__)


@app.route("/login",methods=["POST"])
def index():
    # 接受参数
    user_name=request.form.get("user_name")
    password=request.form.get("password")
    # 参数判断
    if not all([user_name,password]):
        # 所有元素的逻辑判断都为真 则返回真
        resp={
        "code":1,
        "message":"invalid params"
        }
        # 决定返回值
        return jsonify(resp)
    if user_name=="admin" and password=="python":
        resp={
        "code":0,
        "message":"login success"
        }
        return jsonify(resp)
    else:
        resp={
        "code":2,
        "message":"wrong user_name or password"
        }
        return jsonify(resp)

def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()