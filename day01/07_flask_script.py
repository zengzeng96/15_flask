#! /usr/bin/env python3
# -*- coding: utf-8 -*-

# here import the lib

from flask import Flask
from flask_script import Manager  # 启动脚本命令的管理类

app = Flask(__name__)

# 创建管理类的对象
manager = Manager(app)


@app.route("/index")
def index():
    return "index page"


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
