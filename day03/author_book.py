#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-11 20:55:19
# @Author  : ZENG JIA (zengjia42@126.com)
# @Link    : https://weibo.com/5504445825/profile?topnav=1&wvr=6


# here import the lib
from flask_sqlalchemy import SQLAlchemy

from flask import Flask,render_template,request,redirect,url_for,jsonify
from flask_wtf import FlaskForm
from wtforms import  StringField,SubmitField
from wtforms.validators import DataRequired
import json
from flask_script import Manager
from flask_migrate import Migrate,MigrateCommand
app = Flask(__name__)


class Config(object):
    """配置参数"""
    # sqlalchemy的配置参数
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/bj19"  # 指明要连接的数据库
    # sqlalchemy自动跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SECRET_KEY="awewdwfwfwdetet"


app.config.from_object(Config)
db = SQLAlchemy(app)

# 创建flask脚本管理工具对象
manager=Manager(app)
# 创建数据库迁移工具对象
Migrate(app,db)
# 向manager对象中添加数据库的操作命令
manager.add_command("db",MigrateCommand)



# 定义数据库模型
class Author(db.Model):
    """作者"""
    __tablename__ = "tbl_authors"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    email = db.Column(db.String(32), unique=True)
    books = db.relationship("Book", backref="author")


class Book(db.Model):
    """书籍模型类"""
    __tablename__ = "tbl_books"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    lead = db.Column(db.String(20), unique=True)
    author_id = db.Column(db.Integer, db.ForeignKey("tbl_authors.id"))


# 创建表单模型类
class AuthorBookForm(FlaskForm):
    """作者数据表单模型类"""
    author_name=StringField(label=u"作者",validators=[DataRequired("作者必填")])
    book_name=StringField(label=u"书籍",validators=[DataRequired("书籍必填")])
    lead=StringField(label=u"主角",validators=[DataRequired("主角必填")])

    email=StringField(label=u"邮箱",validators=[DataRequired("邮箱必填")])

    submit=SubmitField(label=u"保存")

        
@app.route("/",methods=["GET","POST"])
def index():
    # 创建表单对象
    form=AuthorBookForm()
    if form.validate_on_submit():
        #验证表单成功 提取表单数据
        author_name=form.author_name.data
        email=form.email.data
        book_name=form.book_name.data
        lead=form.lead.data
        # 保存数据库
        author=Author(name=author_name,email=email)
        db.session.add(author)
        db.session.commit()

        # book=Book(name=book_name,author_id=author.id)
        book=Book(name=book_name,lead=lead,author=author)
        # book=
        db.session.add(book)
        db.session.commit()
    # 查询数据库

    author_li=Author.query.all()
    return render_template("author_book.html",authors=author_li,form=form)

# post 方式获取参数
# post /delete_book
#{"book_id":x}
# @app.route("/delete_book",methods=["POST"])
# def delete_book():
#     """删除数据"""
#     # 提取参数
#     # 如果前端发送的请求体数据是json格式 get_json会直接解析成字典
#     # get_json要求前端传送数据 "Content-Type":"application/json"

#     req_dict=request.get_json()
#     print("*"*10,req_dict,"*"*10)
#     # json.loads(req_data.)
#     book_id=req_dict.get("book_id")
#     # 删除数据
#     book=Book.query.get(book_id)
#     db.session.delete(book)
#     db.session.commit()
#     # "Content-Type":"application/json"
#     return jsonify(code=0,message="ok")


# get方式获取参数
# /delete_book?book_id=xx
@app.route("/delete_book",methods=["GET"])
def delete_book():
    """删除数据"""
    # 提取参数
    # 如果前端发送的请求体数据是json格式 get_json会直接解析成字典
    # get_json要求前端传送数据 "Content-Type":"application/json"

    book_id=request.args.get("book_id")
    print("*"*10,book_id,"*"*10)
    
    # 删除数据
    book=Book.query.get(book_id)
    db.session.delete(book)
    db.session.commit()
    # "Content-Type":"application/json"
    return redirect(url_for("index"))

def main():
    # app.run(debug=True)
    # app.run(debug=True,port=8000)
    # 通过manager对象来启动程序
    manager.run()


def insert_sql():
    db.drop_all()
    db.create_all()
    au_xi = Author(name='我吃西红柿', email='xihongshi@163.com')
    au_qian = Author(name='萧潜', email='xiaoqian@126.com')
    au_san = Author(name='唐家三少', email='sanshao@163.com')
    db.session.add_all([au_xi, au_qian, au_san])
    db.session.commit()

    bk_xi = Book(name='吞噬星空', lead='罗峰',author_id=au_xi.id)
    bk_xi2 = Book(name='寸芒', lead='李杨',author_id=au_qian.id)
    bk_qian = Book(name='飘渺之旅', lead='李强',author_id=au_qian.id)
    bk_san = Book(name='冰火魔厨', lead='融念冰',author_id=au_san.id)
    # 把数据提交给用户会话
    db.session.add_all(
        [bk_xi, bk_xi2, bk_qian, bk_san])
    # 提交会话
    db.session.commit()


if __name__ == "__main__":
    main()
    # insert_sql()
