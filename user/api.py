from django.core.cache import cache

# Create your views here.
from libs.https import render_json
from common import errors, keys
from user import logic
from user.froms import  Profile_Form

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



def set_profile(request):
    '''对表单进行数据验证'''
    form=Profile_Form(request.POST)#request.POST是一个类字典,而且里面是from表单提交的所有数据
    if form.is_valid():            #is_valid()函数判断的是值是否是有效的
        profile=form.save(commit=False)         #form.save()这个方法是django框架给我们提供的,会将from中的值自动赋到关联的表中
        profile.id=request.session['uid']       #commit=False是为了防止它创建后直接提交,会在数据库中新添加一条数据,达不到我们的目的
        profile.save()                          #将用户id即profile的id赋予给profile然后保存就实现了修改
        return render_json()
    else:
        return render_json(form.errors,errors.PROFILE_ERR) #form.errors是form中的一些错误信息