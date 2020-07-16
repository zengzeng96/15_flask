#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-07 08:56:50
# @Author  : ZENG JIA (zengjia42@126.com)
# @Link    : https://weibo.com/5504445825/profile?topnav=1&wvr=6


# here import the lib
import sys
import os
import re
from flask import Flask, request

app = Flask(__name__)


# 127.0.0.1:5000/index?city=shezhen#问号后面的字符串叫做 查询字符串
# 接口
@app.route("/index", methods=["GET", "POST"])
def index():
    # request中包含了前端发送过来的所有数据
    # request.data        #前端传输过来的数据
    # 表单格式的数据 
    # city=beijing&time=17&age=37
    # 还有传输过来的文件也是表单数据 
    # request.form#也可以读取表单格式的数据
    # 直接提取请求体中表单格式的数据  是一个类字典的对象
    # args记录查询字符串中的内容
    city = request.args.get("city")

    name = request.form.get("name")  # 获取前端严格表单发送过来的数据
    age = request.form.get("age")
    name_li = request.form.getlist("name")
    # 通过get方法只能拿到多个同名参数中的第一个参数

    print("data数据:", request.data)  # 获取json格式发送过来的数据

    return "hello name=%s,age=%s,city=%s,name_li=%s" % (name, age, city, name_li)

    # return "index page"


# def register():
#     if request.method=="GET":
#         return render(request,"register.html")
#     else:
#         pass


# http:127.0.0.1:5000/upload
@app.route("/upload", methods=["POST"])
def upload():
    """接受前端传送过来的文件"""
    file_obj = request.files.get("pic")
    if file_obj is None:
        # 表示没有传送过来文件
        return "未传送文件"
    # else:
    # 将文件保存到本地
    # 创建一个文件  向文件写内容
    # with open("demo.jpg","wb") as fp:
    #     fp.write(file_obj.read())
    # 直接使用上传的文件对象保存
    file_obj.save("./demo_angle.jpg")
    return "上传成功 angelbaby"


# 上下文管理器
class Foo(object):
    """进入with语句执行的代码 方法  被with调用"""

    def __enter__(self):
        print ("enter called")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """离开with语句执行的方法"""
        print ("exc_type%s" % exc_type)
        print ("exc_val%s" % exc_val)
        print ("exc_tb%s" % exc_tb)


with Foo() as foo:
    # 设置一个异常
    a = 1 / 0
    print("hello python")


def main():
    app.run(debug=True)


# python2字符串
#     str       一个子集       “utf-8”   gbk
#     unicode   所有字符
if __name__ == "__main__":
    main()
