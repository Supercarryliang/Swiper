"""错误码"""

OK=0
# PHONENUM_ERR=1000
# VCODE_ERR=1001
# LOGIN_REQIRED=1002
# USER_DOESNOTEXIST=1003
# PROFILE_ERR=1004





class LogicErr(Exception):
    '''错误的基类'''
    code=None
    data=None
    def __init__(self,data=None):
        self.data=data

    def __str__(self):   #格式化输出对象
        return self.__class__.__name__  #返回错误对象的类的名字

def gen_logic_err(name,code):
    '''动态创建一个错误类'''
    bases=(LogicErr,)    #type()主要是用来动态创建类,有3个参数,第一个参数是类名,第二个是继承的类,是一个元祖
    attr_dict={'code':code}            #第三个参数就是类中的属性,是一个字典
    return type(name,bases,attr_dict)

PhonenumErr=gen_logic_err('PhonenumErr',1000)
VcodeErr=gen_logic_err('VcodeErr',1001)
LoginReqired=gen_logic_err('LoginReqired',1002)
UserDoesNotExist=gen_logic_err('UserDoesNotExist',1003)
ProfileErr=gen_logic_err('Profile_Err',1004)
StypeErr=gen_logic_err('StypeErr',1005)
RewindLimitErr=gen_logic_err('RewindLimitErr',1006)
PermissionRequired=gen_logic_err('PermissionRequired',1007)
