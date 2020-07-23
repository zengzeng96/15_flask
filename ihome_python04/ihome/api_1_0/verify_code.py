# coding:utf-8
from . import api
from ihome.utils.captcha.captcha import captcha
from ihome import redis_store
from ihome import constants, db
from flask import current_app
from flask import jsonify, make_response, request
from ihome.utils.response_code import RET
from ihome.models import User
from ihome.libs.yuntongxun.sms import CCP
import random
from ihome.tasks.sms.tasks import send_sms


# 127.0.0.1/api/v1.0/image_codes/<image_code_id>
@api.route("/image_codes/<image_code_id>")
def get_iamge_code(image_code_id):  # 一般采用Restful风格
    """
    获取图片验证码
    :params image_code_id:图片验证码编号
    :return: 正常：验证码图片   异常：返回json
    """
    # 获取参数
    # 检验参数
    # 业务逻辑处理
    # 生成验证码图片
    # 名字 真实文本 图片数据
    name, text, image_data = captcha.generate_captcha()
    # 将验证码真实值与编号保存到redis中  设置有效期
    # redis_store.set("image_code_%s"%image_code_id,text)
    # redis_store.expire("image_code_%s"%image_code_id,constants.IMAGE_CODE_REDIS_EXPIRES)#设置有效时间
    # 上面的两步可以合并为一个步骤
    try:
        #                             记录的名字               有效期                     记录值
        redis_store.setex("image_code_%s" % image_code_id, constants.IMAGE_CODE_REDIS_EXPIRES, text)
    except Exception as e:
        # 记录日志
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='save image code id failed')
    # 返回图片
    resp = make_response(image_data)
    resp.headers['Content-Type'] = 'image/jpg'
    return resp


# GET /api/v1.0/sms_codes/<mobile>?image_code=xxxx&image_code_id=XXX
# @api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
# def get_sms_code(mobile):
#     """
#     获取短信验证码
#     :param mobile:获取的手机号码 str
#     :return:
#     """
#     # 获取参数
#     image_code = request.args.get('image_code')
#     image_code_id = request.args.get('image_code_id')
#     # 校验参数
#     if not all([image_code, image_code_id]):
#         # 表示参数不完整
#         return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
#     # 业务逻辑处理
#     # 从redis中取出真实的图片验证码
#     try:
#         real_image_code = redis_store.get("image_code_%s" % image_code_id)
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg='redis数据库异常')
#     # 删除redis中的图片验证码 防止用户使用同一个图片验证码验证多次
#     try:
#         redis_store.delete("image_code_%s" % image_code_id)
#     except Exception as e:
#         current_app.logger.error(e)
#
#     # 判断图片验证码是否过期
#     if real_image_code is None:
#         return jsonify(errno=RET.NODATA, errmsg='图片验证码失效')
#     if real_image_code.lower() != image_code.lower():
#         # 表示用户的图片验证码填写错误
#         return jsonify(errno=RET.DATAERR, errmsg='图片验证码错误')
#     # 与用户填写的值进行对比
#     # 判断对于这个手机号的操作在60秒内有没有之前的记录 如果有 则认为用户的操作频繁 不接受处理
#     try:
#         sendflag = redis_store.get("send_sms_code_%s" % mobile)
#     except Exception as e:
#         current_app.logger.error(e)
#
#     else:
#         # 没有出现异常
#         if sendflag is not None:
#             # 表示在60秒内之前有过发送的记录
#             return jsonify(errno=RET.REQERR, errmsg='请求过于频繁，请60秒后重试')
#     # 判断手机号是否存在
#     try:
#         user = User.query.filter_by(mobile=mobile).first()
#     except Exception as e:
#         current_app.logger.error(e)
#     else:  # 没有发生异常则执行下面的语句
#         if user is not None:
#             # 表示手机号已经存在
#             return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")
#
#     # 如果手机号不存在则生成短信验证码
#     sms_code = "%06d" % random.randint(0, 999999)
#     # 保存真实的短信验证码
#     try:
#         redis_store.setex('sms_code_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
#         # 保存发送给这个手机号的记录 防止用户在60秒内再次触发发送短信的操作
#         redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.DBERR, errmsg="保存短信验证码异常")
#     # 发送短信
#     try:
#         ccp = CCP()
#         result = ccp.sendTemplateSMS('13661159228', [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES / 60)], 1)
#     except Exception as e:
#         current_app.logger.error(e)
#         return jsonify(errno=RET.THIRDERR, errmsg='发送异常')
#     if result == 0:
#         # 发送成功
#         return jsonify(errno=RET.OK, errmsg='发送成功')
#     else:
#         return jsonify(errno=RET.THIRDERR, errmsg='发送失败')

# 返回值
# 708 - 30
# 3.4
# 708 - 29
# 8.1
# 707 - 30
# 3.8
@api.route("/sms_codes/<re(r'1[34578]\d{9}'):mobile>")
def get_sms_code(mobile):
    """
    获取短信验证码
    :param mobile:获取的手机号码 str
    :return:
    """
    # 获取参数
    image_code = request.args.get('image_code')
    image_code_id = request.args.get('image_code_id')
    # 校验参数
    if not all([image_code, image_code_id]):
        # 表示参数不完整
        return jsonify(errno=RET.PARAMERR, errmsg='参数不完整')
    # 业务逻辑处理
    # 从redis中取出真实的图片验证码
    try:
        real_image_code = redis_store.get("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg='redis数据库异常')
    # 删除redis中的图片验证码 防止用户使用同一个图片验证码验证多次
    try:
        redis_store.delete("image_code_%s" % image_code_id)
    except Exception as e:
        current_app.logger.error(e)

    # 判断图片验证码是否过期
    if real_image_code is None:
        return jsonify(errno=RET.NODATA, errmsg='图片验证码失效')
    if real_image_code.lower() != image_code.lower():
        # 表示用户的图片验证码填写错误
        return jsonify(errno=RET.DATAERR, errmsg='图片验证码错误')
    # 与用户填写的值进行对比
    # 判断对于这个手机号的操作在60秒内有没有之前的记录 如果有 则认为用户的操作频繁 不接受处理
    try:
        sendflag = redis_store.get("send_sms_code_%s" % mobile)
    except Exception as e:
        current_app.logger.error(e)

    else:
        # 没有出现异常
        if sendflag is not None:
            # 表示在60秒内之前有过发送的记录
            return jsonify(errno=RET.REQERR, errmsg='请求过于频繁，请60秒后重试')
    # 判断手机号是否存在
    try:
        user = User.query.filter_by(mobile=mobile).first()
    except Exception as e:
        current_app.logger.error(e)
    else:  # 没有发生异常则执行下面的语句
        if user is not None:
            # 表示手机号已经存在
            return jsonify(errno=RET.DATAEXIST, errmsg="手机号已存在")

    # 如果手机号不存在则生成短信验证码
    sms_code = "%06d" % random.randint(0, 999999)
    # 保存真实的短信验证码
    try:
        redis_store.setex('sms_code_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 保存发送给这个手机号的记录 防止用户在60秒内再次触发发送短信的操作
        redis_store.setex("send_sms_code_%s" % mobile, constants.SEND_SMS_CODE_INTERVAL, 1)
    except Exception as e:
        current_app.logger.error(e)
        return jsonify(errno=RET.DBERR, errmsg="保存短信验证码异常")

    # try:
    #     ccp = CCP()
    #     result = ccp.sendTemplateSMS('13661159228', [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES / 60)], 1)
    # except Exception as e:
    #     current_app.logger.error(e)
    #     return jsonify(errno=RET.THIRDERR, errmsg='发送异常')
    # 使用celery异步发送短信 delay函数调用后立即返回
    send_sms.delay(mobile, [sms_code, int(constants.SMS_CODE_REDIS_EXPIRES / 60)], 1)
    return jsonify(errno=RET.THIRDERR, errmsg='发送失败')
