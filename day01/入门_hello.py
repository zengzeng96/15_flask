#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-04 21:18:23

# here import the lib
import sys
import os
import re
from flask import Flask,current_app

# 创建Flask应用对象
# __name__表示当前模块的名字
# 模块名 flask以这个模块所在的目录为总目录  默认这个目录中的
# static为静态目录
# templates为模板目录
app=Flask(__name__,#寻找静态目录与模板目录的参数
static_url_path="/python",#访问静态资源的url前缀 默认是 static
#这样写的意思就是只要是以   /python  开头的地址都是静态资源路径 不再去寻找匹配动态资源
static_folder="static",#以当前模块的static目录作为静态目录  静态文件的目录  也可以指定为绝对路径
template_folder="templates"#模板文件的目录 默认是templates
)
# 这个__name__参数基本可以指定为任何值 找不到的话
# flask就会默认到当前目录下来找静态文件的路径
# 但是不能指定为'abc'  因为abc也是python的一个标准块

#配置参数的使用方式
# 1.使用配置文件
# app.config.from_pyfile("config.cfg")

# 2. 使用对象配置方式
class Config(object):
    """docstring for Config"""
    DEBUG=True
    ITCAST="python"

app.config.from_object(Config)

# 3.直接操作config的字典对象
# app.config["DEBUG"]=True


@app.route("/")
def index():#通过装饰器来绑定视图函数
    '''定义视图函数'''
    #读取配置参数
    # 1.直接从全局对象app.config字典中取值
    # print(app.config.get("ITCAST"))
    # 2.通过current_app获取
    print(current_app.config.get("ITCAST"))
    return "Hello flask"


def main():
    pass




if __name__ == "__main__":
    # main()
    # 启动flask程序
    # app.run的参数说明
    app.run(
        # host='192.168.0.109',
        host='0.0.0.0',#任何ip都能访问
        port=5000,
        debug=True)
