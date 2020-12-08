from django.utils.deprecation import MiddlewareMixin

from common import errors
from libs.https import render_json
from user.models import User


class AuthMiddleware(MiddlewareMixin):
    AUTH_URL_WHITE_LIST=[
        '/api/user/get_vcode',
        '/api/user/check_vcode',
    ]
    def process_request(self,request):
        #判断url是否在白名单内
        if request.path in self.AUTH_URL_WHITE_LIST:
            #如果在白名单内直接跳出
            return


        #判断用户是否登录
        uid=request.session.get('uid')
        if uid:
            #很多请求都需要获取一下user所以在中间件中获取
            try:
                request.user=User.objects.get(id=uid)#ruquest.user意思就是将user附加到这次request上
                return
            except User.DoesNotExist:
                return render_json(code=errors.UserDoesNotExist.code)
        else:
            return render_json(code=errors.LoginReqired.code)#如果未登录返回一个错误码给前端




class LogicErrMiddleware(MiddlewareMixin):
    '''捕获异常对象'''
    def process_exception(self,request,exception):  #exception是被捕获的异常对象
        if isinstance(exception,errors.LogicErr):  #isinstance(object, classinfo)object是一个实例对象,是一个类名
           data=exception.data or str(exception)  # 判断当前实例对象是否是该类或其子类下的对象
           return render_json(data=data,code=exception.code)