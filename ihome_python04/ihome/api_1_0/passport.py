#! /usr/bin/env python
# -*- coding:utf-8 -*-
from . import api
from flask import request, jsonify, current_app, session
from ihome.utils.response_code import RET
import re
from ihome import redis_store, db, constants
from ihome.models import User
from sqlalchemy.exc import IntegrityError


# from werkzeug.security import generate_password_hash,check_password_hash
# @api.route("/users", method=['POST'])
@api.route("/users", methods=['POST'])
def register():
    """
    注册
    :param 手机号 短信验证码  密码  确认密码
    参数格式: json格式数据 （前端传过来）
    :return:
    """
    # 获取请求的json数据 返回字典
    req_dict = request.get_json()
    mobile = req_dict.get('mobile')
    sms_code = req_dict.get('sms_code')
    password = req_dict.get('password')
    password2 = req_dict.get('password2')
    # 校验参数
    if not all([mobile, sms_code, password, password2]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    # 判断手机号格式
    if not re.match(r'1[34578]\d{9}', mobile):
        # 表示格式不对
        return jsonify(errno=RET.PARAMERR, errmsg='手机号格式错误')

    if password != password2:
        return jsonify(errno=RET.PARAMERR, errmsg='两次密码不一致')
    # 业务逻辑处理
    # 从redis中取出短信验证码
    try:
        real_sms_code = redis_store.get("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='读取真实短信验证码异常')
    # 判断短信验证码是否过期
    if real_sms_code is None:
        return jsonify(errno=RET.NODATA, errmsg='短信验证码已过期')
    # 删除redis中的短信验证码 防止重复使用校验
    try:
        redis_store.delete("sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger(e)

    # 对比验证码的正确信
    if real_sms_code != sms_code:
        return jsonify(errno=RET.DATAERR, errmsg='短信验证码输入错误')

    # 判断手机号是否注册过
    # try:
    # try:
    #     user = User.query.filter_by(mobile=mobile).first()
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.DBERR, errmsg='数据库异常')
    # else:  # 没有发生异常则执行下面的语句
    #     if user is not None:
    #         # 表示手机号已经存在
    #         return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
    # 保存数据到数据库中
    user = User(name=mobile, mobile=mobile)
    user.password = password  # 设置属性
    # print(user.password)  # 读取属性
    try:
        db.session.add(user)
        db.session.commit()
    except IntegrityError as e:
        # 数据库操作错误的回滚
        db.session.rollback()
        # 表示手机号出现了重复值 说明手机号已经注册了
        current_app.logger(e)
        return jsonify(errno=RET.DATAEXIST, errmsg='手机号已经存在')
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='查询数据库异常')
    # 盐值

    # 保存登录状态到session中
    session['name'] = mobile
    session['mobile'] = mobile
    session['id'] = user.id
    # 返回结果
    return jsonify(errno=RET.OK, errmsg='注册成功')


@api.route("/sessions", methods=['POST'])
def login():
    """
    用户登录
    :param   手机号   密码
    :return:
    """
    # 获取参数
    req_dict = request.get_json()
    mobile = req_dict.get("mobile")
    password = req_dict.get("password")

    # 校验参数
    # 参数完整的校验
    if not all([mobile, password]):
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')

    # 手机号的格式
    if not re.match(r'1[34578]\d{9}', mobile):
        return jsonify(errno=RET.PARAMERR, errmsg='手机号码格式错误')
    # 判断错误次数是否超过限制  如果查过限制 则返回
    # redis中记录访问次数："access_nums_请求的ip":次数
    user_ip = request.remote_addr
    try:
        access_nums = redis_store.get('access_nums_%s' % user_ip)
    except Exception as e:
        current_app.logger.error(e)
    else:
        if access_nums is not None and int(access_nums) >= constants.LOGIN_ERROR_MAX_TIMES:
            return jsonify(errno=RET.REQERR, errmsg='错误次数过多，请稍后重试')
    # 手机号是否存在
    # 判断手机号和密码是否准确
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='获取用户信息失败')
    if user is None or not user.check_password(password):
        # 用户名或密码错误
        # 如果验证失败 则记录错误次数  返回信息
        try:
            redis_store.incr("access_num_%s" % user_ip)
            redis_store.expire("access_num_%s" % user_ip, constants.LOGIN_ERROR_FOBBID_TIME)
        except Exception as e:
            current_app.logger.error(e)
        return jsonify(errno=RET.DATAERR, errmsg='用户名或密码输入错误')

    # 业务处理
    # 如果验证相同成功 保存登录状态
    session['name'] = user.name
    session['mobile'] = user.mobile
    session['user_id'] = user.id

    # 返回结果
    return jsonify(errno=RET.OK, errmsg='登陆成功')


@api.route("/session", methods=["GET"])
def checklogin():
    """
    检查登录状态
    :return:
    """
    # 尝试从session中获取用户的名字
    name = session.get("name")
    # 如果session中的数据name名字存在 则表示用户已经登录 否则未登录
    if name is not None:
        return jsonify(errno=RET.OK, errmsg='true', data={'name': name})
    else:
        return jsonify(errno=RET.SESSIONERR, errmsg='false')


@api.route("/session", methods=["DELETE"])
def logout():
    """
    退出登录
    :return:
    """
    # 清除session数据
    session.clear()
    return jsonify(errno=RET.OK, errmsg='OK')
