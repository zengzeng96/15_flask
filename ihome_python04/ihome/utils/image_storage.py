#! /usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_data, etag, urlsafe_base64_encode
import qiniu.config

# 需要填写你的 Access Key 和 Secret Key
access_key = 'vjiGu0eEBkPhJw3CdHNtxtWlaMVt6o-T2gy7vP5X'
secret_key = 'zhuChYAt112MXOup3QRXYoH_C0kRny9KfkfWkEL1'


def storage(file_data):
    """
    :param  file_data:要上传的文件数据
    上传文件到七牛
    :return:
    """
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'ihome-python04-zeng'
    # 上传后保存的文件名
    # key = 'my-python-logo.png'
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, None, 3600)

    ret, info = put_data(token, None, file_data)
    if info.status_code==200:
        # 表示上传成功 返回文件名
        return ret.get("key")
    else:
        # 上传失败
        raise Exception("上传7牛失败")
    # print(info)
    # print("*" * 40)
    # print(ret)


if __name__ == "__main__":
    with open("test.jpg", 'rb') as f:
        file_data = f.read()
    storage(file_data)
