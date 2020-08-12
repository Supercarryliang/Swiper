from django.core.cache import cache

# Create your views here.
from libs.https import render_json
from common import errors, keys
from user import logic

from user.models import User


def  get_vcode(request):
    phone_num=request.POST.get('phone_num')
    #检查手机号是否合法
    if logic.is_phonenum(phone_num):
        #发送验证码
        logic.send_vcode(phone_num)
        return render_json()
    else:
        return render_json(code=errors.PHONENUM_ERR)




def check_vcode(request):
    """检查验证码"""
    phone_num=request.POST.get('phone_num')
    v_code=request.POST.get('v_code')
    print('v_code是'+v_code)

    # 检查手机号是否合法
    if logic.is_phonenum(phone_num):
        cache_vcode=cache.get(keys.VCODE_KEY%phone_num) #从缓存获取验证码
        print(cache_vcode)
        if v_code==cache_vcode:
            try:     #防止用户第一次进入界面报错所以使用了try
                user=User.objects.get(phonenum=phone_num)
            except User.DoesNotExist:
                #用户不存在,创建一个用户
                user=User.objects.create(phonenum=phone_num,nickname=phone_num)

                #执行登录过程
            request.session['uid']=user.id   #用session保存用户的状态
            return render_json(data=user.to_dict()) #将用户的信息返回给页面
        else:
            return render_json(code=errors.VCODE_ERR)#如果验证码错误.返回一个error
    else:
        return render_json(code=errors.PHONENUM_ERR)


def get_profile(request):
    '''获取用户个人资料'''
    data=request.user.profile.to_dict()
    return  render_json(data=data)