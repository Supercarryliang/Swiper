from django.db import models

# Create your models here.
from libs.orm import ModelMixin
from social.models import Friend
from vip.models import Vip


class User(models.Model,ModelMixin):
    SEX=(
        ('male','男性'),
        ('female','女性')
    )
    LOCATION=(
        ('bj','北京'),
        ('sh','上海'),
        ('wh','芜湖'),
        ('sz','深圳'),
        ('wh','武汉'),
        ('cd','成都'),
    )
    phonenum=models.CharField(max_length=14,unique=True,verbose_name='手机号码')
    nickname=models.CharField(max_length=32,unique=True,verbose_name='昵称')
    sex=models.CharField(max_length=8,choices=SEX,verbose_name='性别')
    birth_year=models.IntegerField(default=2000,verbose_name='出生年份')
    birth_month=models.IntegerField(default=1,verbose_name='出生月份')
    birth_day=models.IntegerField(default=1,verbose_name='出生日')
    #这个个人形象存放的是一个链接,所以最大长度给了256
    avatar=models.CharField(max_length=256,verbose_name='个人形象的url')
    location=models.CharField(max_length=8,choices=LOCATION,verbose_name='长居地')

    #用户的会员等级用唯一的id来记录
    vip_id=models.IntegerField(default=1,verbose_name='权限的id')


    #创建一个方法获取用户的profile属性
    @property   #@property装饰器是将一个方法转换成属性
    def profile(self):
        #如果没有_profile属性才会去执行创建或者获取这个对象与数据库进行交互,
        #如果有了直接就能.出这个属性
        if not hasattr(self,'_profile'):
            #动态添加_profile属性
            self._profile,_=Profile.objects.get_or_create(id=self.id)
        return self._profile

    @property
    def vip(self):
        '''用户的会员信息'''
        if not hasattr(self,'_vip'):
            self._vip=Vip.objects.get(id=self.vip_id)
        return self._vip

    @property
    def friends(self):
        '''user的所有好友'''
        friend_id_list=Friend.friend_sid(self)
        friends_info=[friend.to_dict() for friend in User.objects.filter(id__in=friend_id_list)]
        return friends_info

    # def to_dict(self):
    #     return {
    #         'phonenum':self.phonenum,
    #         'nickname':self.nickname,
    #         'sex':self.sex,
    #         'birth_year':self.birth_year,
    #         'birth_month':self.birth_month,
    #         'birth_day':self.birth_day,
    #         'avatar':self.avatar,
    #         'location':self.location,
    #
    #     }



    class Meta:
        db_table='user'

class Profile(models.Model,ModelMixin):
    SEX = (
        ('male', '男性'),
        ('female', '女性')
    )
    LOCATION = (
        ('bj', '北京'),
        ('sh', '上海'),
        ('ah', '安徽'),
        ('sz', '深圳'),
        ('wh', '武汉'),
        ('cd', '成都'),
    )
    location=models.CharField(max_length=8,verbose_name='⽬标城市',choices=LOCATION)
    dating_sex=models.CharField(max_length=8,choices=SEX,verbose_name='匹配的性别')
    min_distance=models.IntegerField(default=1,verbose_name='最小查找范围')
    max_distance=models.IntegerField(default=10,verbose_name='最⼤查找范围')
    min_dating_age=models.IntegerField(default=22,verbose_name='最⼩交友年龄')
    max_dating_age=models.IntegerField(default=50,verbose_name='最⼤交友年龄')
    vibration=models.BooleanField(default=True,verbose_name='开启震动')
    only_matche=models.BooleanField(default=True,verbose_name='不让为匹配的⼈看我的相册')
    auto_play=models.BooleanField(default=True,verbose_name='⾃动播放视频')


    class Meta:
        db_table='profile'




