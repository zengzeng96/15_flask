#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-07 13:17:10
# @Author  : ZENG JIA (zengjia42@126.com)
# @Link    : https://weibo.com/5504445825/profile?topnav=1&wvr=6


# here import the lib
from flask import Flask, session

app = Flask(__name__)
# flask会需要用到的密钥字符串
app.config["SECRET_KEY"]="sahduwhduwudhuwhwuh"
# 在使用session的时候必须要有上面的代码
# flask默认把session保存到cookie中

@app.route("/login")
def login():
    # 设置session数据
    session["name"] = "python"
    session["mobile"] = "13661159228"
    return "login_sucess"


@app.route("/index")
def index():
    # 获取session数据
    name = session.get("name")
    return "hello %s" % name


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
