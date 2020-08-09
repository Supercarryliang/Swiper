from django.db import models

# Create your models here.


class User(models.Model):
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
    phonenum=models.CharField(max_length=14,verbose_name='手机号码')
    nickname=models.CharField(max_length=32,verbose_name='昵称')
    sex=models.CharField(max_length=8,choices=SEX,verbose_name='性别')
    birth_year=models.IntegerField(default=2000,verbose_name='出生年份')
    birth_month=models.IntegerField(default=1,verbose_name='出生月份')
    birth_day=models.IntegerField(default=1,verbose_name='出生日')
    #这个个人形象存放的是一个链接,所以最大长度给了256
    avatar=models.CharField(max_length=256,verbose_name='个人形象')
    location=models.CharField(max_length=8,choices=LOCATION,verbose_name='长居地')


    class Meta:
        db_table='user'
