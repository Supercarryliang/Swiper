

'''编写权限装饰器函数'''
from common import errors


def need_perm(perm_name):
    def demo(view_func):
        def warpper(request):
            if request.user.vip.has_perm(perm_name): #判断当前用户是否有这个权限
                return view_func(request)    #如果有就可以执行这个函数
            else:
                raise errors.PermissionRequired              #没有就抛出一个异常
        return warpper
    return demo