#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# @Date    : 2020-03-11 15:40:46
# @Author  : ZENG JIA (zengjia42@126.com)
# @Link    : https://weibo.com/5504445825/profile?topnav=1&wvr=6


# here import the lib
import sys
import os
import re
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


class Config(object):
    """配置参数"""
    # sqlalchemy的配置参数
    SQLALCHEMY_DATABASE_URI = "mysql://root:root@127.0.0.1:3306/bj19"  # 指明要连接的数据库
    # sqlalchemy自动跟踪数据库
    SQLALCHEMY_TRACK_MODIFICATIONS = True


app.config.from_object(Config)

# 创建数据库sqlalchemy工具对象
db = SQLAlchemy(app)


# 表名的常见规范
# bj19  将数据库的名字作为表名前缀  bj19_
# tbl作为前缀   tbl_
# 创建数据库模型类

class Role(db.Model):
    """用户角色/身份表"""
    __tablename__ = "tbl_roles"
    id = db.Column(db.Integer, primary_key=True)  # Column是指真实存在的数据
    name = db.Column(db.String(32), unique=True)
    users = db.relationship("User", backref="role")  # 不会在表中存在 用于查询
    # backref不能离开role_id外键

    def __repr__(self):
        # 定义之后 可以在显示对象的时候更直观
        return "Role object:name=%s" % self.name


class User(db.Model):
    """用户模型类   用户表"""
    __tablename__ = "tbl_users"  # 表名

    id = db.Column(db.Integer, primary_key=True)  # 整型的数据会默认设置为自增逐渐
    name = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(128), unique=True)
    password = db.Column(db.String(128))
    role_id = db.Column(db.Integer, db.ForeignKey("tbl_roles.id"))  # 外键

    def __repr__(self):
        # 定义之后 可以在显示对象的时候更直观
        return "User object:name=%s" % self.name


@app.route("/")
def index():
    return "index page"


def main():
    # 清楚数据库里的所有数据
    db.drop_all()
    # 创建所有的表
    db.create_all()

    # 创建对象
    role1 = Role(name="admin")
    # session记录对象任务
    db.session.add(role1)
    # 提交任务到数据库中
    db.session.commit()

    role2 = Role(name="stuff")
    # session记录对象任务
    db.session.add(role2)
    # 提交任务到数据库中
    db.session.commit()

    us1 = User(name='wang', email='wang@163.com',
               password='123456', role_id=role1.id)
    us2 = User(name='zhang', email='zhang@189.com',
               password='201512', role_id=role2.id)
    us3 = User(name='chen', email='chen@126.com',
               password='987654', role_id=role2.id)
    us4 = User(name='zhou', email='zhou@163.com',
               password='456789', role_id=role1.id)
    # 一次保存多条数据
    db.session.add_all([us1, us2, us3, us4])
    db.session.commit()
    # 查询数据
    # Role.query.all()#查询所有的数据
    # Role.query.first()#返回第一条记录
    # Role.query.get(2)#只能接受主键 id 值  获取对象
    # db.session.query(Role).all()

    # 过滤   filter_by
    # User.query.filter_by(name="wang").all()
    # User.query.filter_by(name="wang").first()
    # User.query.filter_by(name="wang",role_id=1).first()
    # 不存在的话不会跑抛出异常   会返回None类型

    # 过滤   filter
    # from sqlalchemy import or_
    # User.query.filter(User.name=="wang",User.role_id==1).first()
    # User.query.filter(or_(User.name=="wang",User.email.endswith("163.com"))).all()

    # User.query.offset(2).all()#跳过前面的两条
    # User.query.offset(1).limit(2).all()
    # User.query.order_by("-id").all()
    # User.query.order_by(User.id.desc()).all()#以降序方式排列  默认升序

    # 分组   group_by
    # from sqlalchemy import func
    # db.session.query(User.role_id,func.count(User.role_id)).group_by("User.role_id").all()

    # 关联插查询
    # ro=Role.query.get(1)
    # ro.users
    # ro.users[0]
    # ro.users[1]

    # user=User.query.get(1)
    # user.role_id
    # Role.query.get(user.role_id)
    # 可以通过如下更简便的方式来获取
    # user.role
    # 修改
    # user.name="python"
    # db.session.add(user)
    # db.session.commit()

    # 在查询的时候进行更改
    # User.query.filter_by(name="zhou").update({"name":"itcast","email":"zengjia42@126.com"})
    # ab.session.commit()

    # 删除数据
    # user=User.query.get(3)
    # db.session.delete(user)
    # db.session.commit()





if __name__ == "__main__":
    main()
