import  re
import random
import requests

from Swiper import config


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
    response=send_sms(v_code,phone_num) #发送验证码

    #检查发送状态是否成功
    if response.status_code==200:
        result=response.json()
        if result.get('code')=='000000':
            return True
    return False