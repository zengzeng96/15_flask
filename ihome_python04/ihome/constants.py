# -*- coding:utf-8 -*-

# 图片验证码图片的  redis  有效期  秒
# from ihome.api_1_0.passport import login

IMAGE_CODE_REDIS_EXPIRES = 180
# 设置短信验证码的有效期  秒
SMS_CODE_REDIS_EXPIRES = 300
# 发送短信验证码的间隔    秒
SEND_SMS_CODE_INTERVAL = 60
# 登陆错误尝试的次数
LOGIN_ERROR_MAX_TIMES = 10
# 登陆错误限制的事件
LOGIN_ERROR_FOBBID_TIME = 600
# 七牛的域名
QINIU_URL_DOMAIN = 'http://qdv1xj3n4.bkt.clouddn.com/'
# 城区信息的缓存时间  秒
AREA_INFO_REDIS_CACHE_EXPIRES = 7200
