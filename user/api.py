from django.shortcuts import render

# Create your views here.
from user import logic


def  get_vcode(request):
    phone_num=request.POST.get('phone_num')
    #检查手机号是否合法
    if logic.is_phonenum(phone_num):
        #发送验证码
        logic.send_vcode(phone_num)

    return



def check_vcode(request):
    return