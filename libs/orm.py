from django.db import models

from common import keys
from libs.cache import rds


def to_dict(self,*exclude):
    dict_list={}
    for field in self._meta.fields:  #遍历当前对象的所有属性值
        name=field.attname           #获取所有属性的名字
        if name not in exclude:      #如果属性不在忽略的名单内就放入到字典中显示
            dict_list[name]=getattr(self,name)
    return dict_list






#模仿原生get代码,实现自动生成缓存的get方法
@classmethod
def get(cls,*args, **kwargs):
    """
           Performs the query and returns a single object matching the given
           keyword arguments.
    """

    #检查参数中是否有主键,如果有就能查到相应的key
    if 'id' in kwargs or 'pk' in kwargs:
        pk=kwargs.get('id') or kwargs.get('pk')

        #创建缓存key
        model_key=keys.MODEL_KEY%(cls.__name__,pk)
        #先从缓存获取缓存数据
        model_obj=rds.get(model_key)

        #判断获取到的缓存对象是否是不为空,并且是当前类的一个实例,如果是表明缓存是正确的
        if model_obj is not None and isinstance(model_obj,cls):

            return model_obj

    #如果缓存中未取到,去数据库中去获取
    model_obj=cls.objects.get(*args,**kwargs)


    #生成缓存的key
    model_key=keys.MODEL_KEY%(cls.__name__,model_obj.pk)
    #将数据库中取出的数据写到缓存中
    rds.set(model_key,model_obj,ex=86400*7)  #设置过期时间为7天

    return model_obj



@classmethod
def get_or_create(cls, defaults=None, **kwargs):
    """
    Looks up an object with the given kwargs, creating one if necessary.
    Returns a tuple of (object, created), where created is a boolean
    specifying whether an object was created.
    """
    # 检查参数中是否有主键,如果有就能查到相应的key
    if 'id' in kwargs or 'pk' in kwargs:
        pk = kwargs.get('id') or kwargs.get('pk')

        # 创建缓存key
        model_key = keys.MODEL_KEY % (cls.__name__, pk)
        # 先从缓存获取缓存数据
        model_obj = rds.get(model_key)

        # 判断获取到的缓存对象是否是不为空,并且是当前类的一个实例,如果是表明缓存是正确的
        if model_obj is not None and isinstance(model_obj, cls):
            return model_obj,False

    # 如果缓存中未取到,去数据库中去获取
    model_obj,created= cls.objects.get_or_create(defaults, **kwargs)

    # 生成缓存的key
    model_key = keys.MODEL_KEY % (cls.__name__, model_obj.pk)
    # 将数据库中取出的数据写到缓存中
    rds.set(model_key,model_obj,ex=86400*7)  #设置过期时间为7天

    return model_obj,created


def save(self, force_insert=False,force_update=False,
    using=None,update_fields=None,):
    """Docstring:
    Saves the current instance. Override this in a subclass if you want to
    control the saving process.

    The 'force_insert' and 'force_update' parameters can be used to insist
    that the "save" must be an SQL insert or update (or equivalent for
    non-SQL backends), respectively. Normally, they should not be set.
    """
    #先执行原生的save方法 ,将数据保存到数据库
    self._save(force_insert,force_update,using,update_fields)


    #修改缓存数据
    model_key=keys.MODEL_KEY%(self.__class__.__name__,self.pk)
    rds.set(model_key,self,ex=86400*7)  #设置过期时间为7天




def patch_model():
    """通过MonkeyPatch的方式扩充Model的功能"""
    #为Model添加to_dict
    models.Model.to_dict=to_dict


    #为Model添加get和get_or_create两个类方法
    models.Model.get=get
    models.Model.get_or_create=get_or_create

    #重新定义Model.save,将自定义的save动态添加到model.save方法上
    models.Model._save=models.Model.save
    models.Model.save=save

