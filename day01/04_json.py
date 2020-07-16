#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-07 11:33:34
# @Author  : ZENG JIA (zengjia42@126.com)
# @Link    : https://weibo.com/5504445825/profile?topnav=1&wvr=6


# here import the lib
from flask import Flask, jsonify, make_response, request
import json

app = Flask(__name__)


@app.route("/index")
def index():
    # 返回json信息
    # json就是字符串
    data = {
        "name": "zengjia",
        "age": 24
    }

    # json.dumps()  # 将python的字典转化为json字符串
    # json.loads()  # 将python的json字符串转化为python字典
    # json_str=json.dumps(data)
    # return json_str,200,{"Content-Type":"application/json"}
    # return jsonify(data)
    return jsonify(city="beijing", name="zengjia")


@app.route("/set_cookie")
def set_cookie():
    resp = make_response("success")
    # 设置cookie 默认有效期是临时cookie   浏览器关闭就失效
    resp.set_cookie("Itcast", "python")
    resp.set_cookie("city", "chengdu")
    # max_age设置cookie有效期    单位  s
    resp.set_cookie("city_forever", "beijing", max_age=3600)
    resp.headers["Set-Cookie"]='city_tt=shanghai; Expires=Sat, 07-Mar-2020 05:33:37 GMT; Max-Age=3600; Path=/'
    return resp


@app.route("/get_cookie")
def get_cookie():
    c = request.cookies.get("Itcast")
    return c

@app.route("/delete_cookie")
def delete_cookie():
    resp=make_response("del success")
    #删除cookie
    resp.delete_cookie("Itcast")

    return resp


def main():
    app.run(debug=True)


if __name__ == "__main__":
    main()
