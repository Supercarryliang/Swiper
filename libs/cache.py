from redis import Redis as _Redis
from pickle import dumps,loads
from Swiper import settings
#重新创建Redis继承本来的Redis类
class Redis(_Redis):

    #重写原来的get和set方法,使它的作用跟django的缓存get和set效果基本一致
    def get(self,name):
        """
            Return the value at key ``name``, or None if the key doesn't exist
        """
        #先通过redis的get方法获取到它的数据
        pickled=super().get(name)
        try:
            # 通过loads方法返回它原来的数据,当pickled不是2进制字符串是会出现TypeError,
            return loads(pickled)      #此时用try自动抛出异常
        except TypeError:
            return pickled



    def set(self, name, value,
            ex=None, px=None, nx=False, xx=False, keepttl=False):
        """
        Set the value at key ``name`` to ``value``

        ``ex`` sets an expire flag on key ``name`` for ``ex`` seconds.

        ``px`` sets an expire flag on key ``name`` for ``px`` milliseconds.

        ``nx`` if set to True, set the value at key ``name`` to ``value`` only
            if it does not exist.

        ``xx`` if set to True, set the value at key ``name`` to ``value`` only
            if it already exists.

        ``keepttl`` if True, retain the time to live associated with the key.
            (Available since Redis 6.0)
        """
        #将数据进行序列化
        pickled=dumps(value)

        #使用父类的方法进行set
        return super().set(name,pickled,ex,px,nx,xx)

#创建一个Redis的对象,使其成为一个全局变量,减少连接redis的操作
rds=Redis(**settings.REDIS)    #**(字典)或*(元祖,列表)加参数是一种特殊的传参方式,当函数内需要的参数
                            # 与传入的参数个数相同时,可以使用**或*的方法简化传参