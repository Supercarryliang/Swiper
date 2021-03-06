import os
import  re
import random
import requests
from django.conf import settings
from django.core.cache import cache

from Swiper import config
from common.keys import VCODE_KEY
from libs.qncloud import qn_upload
from worker import celery_app


def is_phonenum(phone_num):
    #检查是否是一个正常的手机号
    if re.match(r'1[3456789]\d{9}$',phone_num):
        return  True
    else:
        return False


def gen_random_vcode(length=4):
    '''产生一个随机的验证码'''
    rand_num=random.randrange(0,10**length)
    #%04d的意思就是位数不足的用0补齐,
    # 此时当length改变时是无法将length直接传递到补齐到第几位的,
    # 所以此时用template变量来实现%04d的效果
    template='%%0%sd'%length
    #此时template即是%0lengthd,vcode就是%0lengthd%rand_num
    v_code=template%rand_num
    return v_code

def send_sms(v_code,phone_num):
    #发送短信
    #使用onfig.YZX_SMS_ARGUS的复制是为了不改变原配置信息,防止其他用户使用时冲突
    args=config.YZX_SMS_ARGUS.copy()
    args['param']=v_code
    args["mobile"]=phone_num
    response=requests.post(url=config.YZX_SMS_URL,json=args)
    return response


def send_vcode(phone_num):
    '''发送验证吗'''
    v_code=gen_random_vcode(4)     #产生一个随机的验证码

    print('------------------>',v_code)
    response=send_sms(v_code,phone_num) #发送验证码

    #检查发送状态是否成功
    # if response.status_code==200:
    #     result=response.json()
    #     if result.get('code')=='000000':
    key=VCODE_KEY%phone_num#为了以后能快速标识
    cache.set(key,v_code,180)#将验证码添加到缓存中
    print(cache.get(key))
    #         return True
    # return False


def save_upload_file(upload_file,uid):
    """保存上传文件到本地"""

    file_name='Avatar-%s.png'%uid               #文件名称
    full_path=os.path.join(settings.MEDIA_DIRS,file_name)  #文件的完整路径
    with open(full_path,'wb') as fp:
        for chunk in upload_file.chunks():
            fp.write(chunk)

    return full_path,file_name



@celery_app.task   #用装饰器实现对该方法的异步处理
def save_avatar(user,avatar):
    '''上传个人头像'''
    full_path, file_name = save_upload_file(avatar, user.id)  # 保存文件到本地
    _, avatar_url = qn_upload(file_name, full_path)  # 上传文件到七牛云
    user.avatar = avatar_url  # 将文件url给user
    user.save()