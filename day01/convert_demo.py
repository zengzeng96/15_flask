#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-05 10:00:49
# @Author  : ZENG JIA (zengjia42@126.com)
# @Link    : https://weibo.com/5504445825/profile?topnav=1&wvr=6


# here import the lib
from flask import Flask, redirect
from werkzeug.routing import BaseConverter

app = Flask(__name__)


# 转换器
# http://127.0.0.1:5000/goods/123
# @app.route("/goods/<int:goods_id>")
@app.route("/goods/<goods_id>")  # 不加转换器类型  默认是普通的字符串规则  除了  / 的任意字符
def goods_detail(goods_id):
    return "goods detail page %s" % goods_id


class MobileConverter(BaseConverter):
    """docstring for MobileConverter"""

    def __init__(self, url_map, regex):
        super(MobileConverter, self).__init__(url_map)
        self.regex = r'1[345678]\d{9}'


# 1.定义自己的转换器
class RegexConverter(BaseConverter):
    """"""

    def __init__(self, url_map, regex):
        # 调用父类的初始化方法
        super(RegexConverter, self).__init__(url_map)
        # 将正则表达式的参数保存到对象的属性中 flask会去使用这个属性来进行正则的路由匹配
        self.regex = regex

        def to_python(self, value):
            # 正则表达式匹配的值会传入该函数   value
            print("to_python方法被调用")
            # return "abc"
            return value

        def to_url(self, value):
            # 使用url_for方法的时候被调用
            print("to_url方法被调用")
            # return "13661159228"
            return value


# 2.将自定义的转换器添加到flask应用中
app.url_map.converters["re"] = RegexConverter
app.url_map.converters["mobile"] = MobileConverter


# @app.route("/send/<re(r'1[345678]\d{9}'):mobile>")
@app.route("/send/<mobile:mobile_num>")
def send_sms(mobile_num):
    return "send sms to %s" % mobile_num


@app.route("/index")
def index():
    url = url_for("send_sms", mobile_num="18911112222")
    return redirect(url)


if __name__ == "__main__":
    # 查看整个flask中的路由信息
    print(app.url_map)
    # 启动flask程序
    app.run(debug=True)
