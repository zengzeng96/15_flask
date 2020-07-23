# -*- coding: UTF-8 -*-

from CCPRestSDK import REST
import ConfigParser

# 主帐号
accountSid = '8aaf0708732220a601736f20ff041f44'

# 主帐号Token
accountToken = '506dc1a3d8224e848ce0e7e0412d67a4'

# 应用Id
appId = '8aaf0708732220a601736f2100061f4b'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id
class CCP(object):
    """用于自己发送短线的辅助类
    :param
    """
    _singleton = None  # 类属性是共用的

    def __new__(cls, *args, **kwargs):
        if cls._singleton is None:
            obj = object.__new__(cls, *args, **kwargs)
            obj.rest = REST(serverIP, serverPort, softVersion)
            obj.rest.setAccount(accountSid, accountToken)
            obj.rest.setAppId(appId)
            cls._singleton = obj
        return cls._singleton

    # instance = None
    #
    # def __new__(cls, *args, **kwargs):
    #     if cls.instance is None:
    #         cls.instance = super().__new__(cls,*args, **kwargs)
    #     return cls.instance

    def sendTemplateSMS(self, to, datas, tempId):
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        # for k, v in result.iteritems():
        #
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)
        # statusCode:000000
        status_code = result.get("statusCode")
        if status_code == '000000':
            # 表示发送短信成功
            return 0
        else:
            # 发送失败
            return -1


if __name__ == "__main__":
    ccp = CCP()
    ret = ccp.sendTemplateSMS('13661159228', ['1234', '5'], 1)
    print(ret)

# sendTemplateSMS(手机号码,内容数据,模板Id)
