from django.db import models

# Create your models here.
from django.db.models import Q

from common import errors


class Swiped(models.Model):

    types=(
        ('dislike','左滑'),
        ('like','右滑'),
        ('superlike','上滑'),
    )
    uid=models.IntegerField(verbose_name='滑动用户的id')
    sid=models.IntegerField(verbose_name='被滑动用户的id')
    s_type=models.CharField(max_length=12,choices=types,verbose_name='滑动类型')
    s_time=models.DateTimeField(auto_now_add=True,verbose_name='滑动时间')

    class Meta:
        db_table='swiped'

    @classmethod                #使用类方法
    def swipe(cls,uid,sid,s_type):
        '''创建一个滑动记录'''
        if s_type not in ('dislike','like','superlike'):
            raise errors.StypeErr
        #为了防止重复创建使用get_or_create方法
        swipe,_=cls.get_or_create(uid=uid,sid=sid,s_type=s_type)
        return swipe

    @classmethod
    def is_liked(cls,uid,sid):
        '''判断是否喜欢过'''
        return cls.objects.filter(uid=uid,sid=sid,s_type__in=['like','superlike']).exists()


    @classmethod
    def who_liked_me(cls,uid):
        '''获取谁喜欢过我的用户id'''
        liked_me_uid_list=cls.objects.filter(sid=uid,s_type__in=['like','superlike']).values_list('uid')
        return liked_me_uid_list
#好友列表的模型
class Friend(models.Model):
    sid1=models.IntegerField(verbose_name='相互关注的用户id1')
    sid2=models.IntegerField(verbose_name='相互关注的用户id2')

    @classmethod
    def make_friends(cls,sid1,sid2):
        '''成为好友'''
        sid1,sid2=(sid2,sid1) if sid1>sid2 else (sid1,sid2)  #为了减少数据库操作,将两个id进行比较 小的放在前面
        friend,_=cls.get_or_create(sid1=sid1,sid2=sid2)       #添加一条好友记录
        return friend

    @classmethod
    def is_friend(cls,sid1,sid2):
        '''检查两个用户是否是好友'''
        sid1, sid2 = (sid2, sid1) if sid1 > sid2 else (sid1, sid2)
        if cls.objects.filter(sid1=sid1,sid2=sid2).exists():
            return True
        else:
            return False
    @classmethod
    def friend_sid(cls,user):
        '''获取好友id'''
        condition=Q(sid1=user.id)|Q(sid2=user.id)  #使用Q对象对用户id进行筛选,因为当前用户id有可能在前面
        friend_list=cls.objects.filter(condition)  #也有可能在后面
        friend_id_list=[]
        for friend in friend_list:
            #判断当前用户id如果在前面,就将friend对象的后面的sid赋值给sid,否则就将前面sid给sid
            sid=friend.sid2 if friend.sid1==user.id else friend.sid1
            friend_id_list.append(sid)
        return friend_id_list

    @classmethod
    def remove_friend(cls,sid1,sid2):
        sid1, sid2 = (sid2, sid1) if sid1 > sid2 else (sid1, sid2)
        cls.objects.filter(sid1=sid1,sid2=sid2).delete()

    class Meta:
        db_table='friend'