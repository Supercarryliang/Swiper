#!/usr/bin/env python
import os
import sys
import random
import django


#设置环境

BASE_DIR=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#其中第一个dirname是项目名字即Swiper  第二个dirname是scripts  第二个__file__就是当前文件的名字init.py
#所以BASE_DIR就是Swiper/scripts/init.py
sys.path.insert(0,BASE_DIR)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Swiper.settings")
django.setup()

from user.models import User
from vip.models import Vip, Permission, VipPermRelation

last_names=(
'赵钱孙李周吴郑王'
'冯陈褚卫蒋沈韩杨'
'朱秦尤许何吕施张'
'孔曹严华金魏陶姜'
'戚谢邹喻柏水窦章'
'云苏潘葛奚范彭郎'
)

first_names={
    'male':
        [
          '奕铭','小明','茅台','闰土',
          '大白','王炸','蘑菇','妹爷'
        ],
    'female':
        [
          '球球','米线','冷萌','小花',
          '小雪','小米','小苍','绛紫',
        ]
}

def range_name():
    last_name=random.choice(last_names)
    sex=random.choice(list(first_names.keys()))  #生成随机的性别
    first_name=random.choice(first_names[sex])

    return last_name+first_name,sex


def create_robot(n):
    #创建初始用户
    for i in range(n):
        name, sex = range_name()
        try:
            User.objects.create(
                phonenum='%s'%random.randint(21000000000,219000000000),
                nickname=name,
                sex=sex,
                birth_year=random.randint(1980,2000),
                birth_month=random.randint(1,12),
                birth_day=random.randint(1,28),
                location=random.choice(['bj','sh','ah','sz','wh','cd'])

            )
            print('created:%s%s'%(name,sex))
        except django.db.utils.IntegrityError:
            pass




def vip_init():
    '''初始化vip表'''
    for i in range(4):
        vip,_=Vip.objects.get_or_create(
            name='%s级会员'%i,
            level=i,
            price=5.0*i,
        )
        print('创建了会员%s'%i)


def permission_init():
    '''初始化权限表'''
    permission_description=(
        ('superlike','超级喜欢',),
        ('rewind','反悔',),
        ('show_liked_me','查看喜欢过我的人',)
    )

    for name,des in permission_description:
            permission,_=Permission.objects.get_or_create(
                name=name,description=des
            )



def vip_perm_init():
    '''会员权限关系表初始化'''
    #获取vip
    vip1=Vip.objects.get(level=1)
    vip2=Vip.objects.get(level=2)
    vip3=Vip.objects.get(level=3)

    #获取权限
    superlike=Permission.objects.get(name='superlike')
    rewind=Permission.objects.get(name='rewind')
    show_liked_me=Permission.objects.get(name='show_liked_me')

    #创建1级会员权限
    VipPermRelation.objects.get_or_create(vip_id=vip1.id,perm_id=superlike.id)


    #创建2级会员权限
    VipPermRelation.objects.get_or_create(vip_id=vip2.id,perm_id=superlike.id)
    VipPermRelation.objects.get_or_create(vip_id=vip2.id,perm_id=rewind.id)


    #创建3级会员权限
    VipPermRelation.objects.get_or_create(vip_id=vip3.id,perm_id=superlike.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id,perm_id=rewind.id)
    VipPermRelation.objects.get_or_create(vip_id=vip3.id,perm_id=show_liked_me.id)




















if __name__=='__main__':
    # create_robot(100)
    vip_init()
    permission_init()
    vip_perm_init()