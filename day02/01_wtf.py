#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-09 12:51:16
# @Author  : ZENG JIA (zengjia42@126.com)
# @Link    : https://weibo.com/5504445825/profile?topnav=1&wvr=6


# here import the lib
import sys
import os
import re
from flask import Flask,render_template,redirect,url_for,session
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired,EqualTo
app=Flask(__name__)
app.config["SECRET_KEY"]="bhasejfsehfgewhgerhg"
# 定义表单的模型类
class RegisterForm(FlaskForm):
    """自定义的注册表单模型类"""
    # def __init__(self, arg):
    #     super(RegisterForm, self).__init__()
    #     self.arg = arg
    #                                             说明标签              验证器   
    # DataRequired   保证数据必须填写 并且不能为空
    user_name=StringField(label=u"用户名",validators=[DataRequired(u"用户名不能为空")])
    password=PasswordField(label=u"密码",validators=[DataRequired(u"密码不能为空")])
    password2=PasswordField(label=u"确认密码",validators=[DataRequired(u"确认密码不能为空"),EqualTo("password",u"两次密码不一致")])
    submit=SubmitField(label=u"提交")

@app.route("/register",methods=["GET","POST"])
def register():
    # 创建表单对象  如果是post请求 前端发送了数据 flask会把数据在构造form对象的时候 存放到对象中 

    form=RegisterForm()
    # 判断form中的数据是否合理
    # 如果form中的所有数据完全满足验证器，则返回真，否则返回假
    if form.validate_on_submit():
        # 表示验证合格
        # 提取数据
        uname=form.user_name.data
        pwd=form.password.data
        pwd2=form.password2.data
        session["user_name"]=uname
        # session["password"]=pwd

        print(uname,pwd,pwd2)
        return redirect(url_for("index"))

    return render_template("register.html",form=form)

@app.route("/index")
def index():
    user_name=session.get("user_name","")
    return "hello %s"%user_name

def main():
    # app.run(debug=True)
    app.run()


if __name__ == "__main__":
    main()