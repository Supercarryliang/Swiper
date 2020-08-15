# -*- coding: utf-8 -*-
from urllib.parse import urljoin

from qiniu import Auth, put_file, etag
from Swiper import config
#需要填写你的 Access Key 和 Secret Key
def qn_upload(filename,filepath):
    '''将文件上传到七牛云中'''
    # filepath要上传文件的本地路径
    # filename要上传文件名字
    qn = Auth(config.QN_ACCESS_KEY,config.QN_SECRET_KEY)#构建鉴权对象
    token = qn.upload_token(config.QN_BUCKET, filename, 3600)    #生成上传 Token，并指定过期时间
    ret, info = put_file(token, filename, filepath)             #文件上传
    if info.ok():                                               #如果上传文件成功
        avatar_url=urljoin(config.QN_BASE_URL,filename)         #将文件所在的url返回给
        return True,avatar_url
    else:
        return False,''