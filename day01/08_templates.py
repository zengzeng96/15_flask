#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-08 11:11:28
# @Author  : ZENG JIA (zengjia42@126.com)
# @Link    : https://weibo.com/5504445825/profile?topnav=1&wvr=6


# here import the lib
from flask import Flask, render_template
from flask_script import Manager  # 启动脚本命令的管理类

app = Flask(__name__)

# 创建管理类的对象
manager = Manager(app)


@app.route("/index")
def index():
    data = {
        "name": "python",
        "age": 18,
        "my_dict": {"city": "shenzhen"},
        "my_list": [1, 2, 3, 4, 5,6,7],
        "my_int": 0,
    }
    # return render_template("index.html", name="python", age=18)
    return render_template("index.html", **data)
# 自定义过滤器
# 1.过滤器函数

def list_step_2(li):
    """自定义的过滤器"""
    return li[::2]
# 注册过滤器
app.add_template_filter(list_step_2,"li2")
#li2是自己指定的名称

#2.通过装饰器来实现
@app.template_filter("li3")
def list_step_3(li):
    # 装饰器函数中指定过滤器的名称
    """自定义的过滤器"""
    return li[::3]


def main():
    # app.run(debug=True)
    # 通过manager对象来启动flask
    # 启动命令
    # python 07_flask_script.py runserver

    # 进入python交互器
    # python 07_flask_script.py shell
    manager.run()


if __name__ == "__main__":
    main()
