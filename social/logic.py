import datetime

from django.core.cache import cache
from django.http import HttpResponse

from Swiper import config
from common import keys, errors
from social.models import Swiped, Friend
from user.models import User


def get_recommond_list(user,limit):
    '''获取推荐列表'''
    #进行年龄筛选
    curr_year=datetime.date.today().year  #获取当前年份
    max_birth_year=curr_year-user.profile.min_dating_age #获取最大出生年份
    min_birth_year=curr_year-user.profile.max_dating_age #获取最小出生年份
    print(max_birth_year,min_birth_year)
    #排除那些被滑动之后的用户id
    sid_list=Swiped.objects.filter(uid=user.id).values_list('sid',flat=True) #values_list()是返回一个‘sid’属性的列表
    #进行过滤  找到符合当前用户要求的推荐用户
    rcmd_users=User.objects.filter(
        location=user.profile.location,
        sex=user.profile.dating_sex,
        birth_year__lt=max_birth_year,
        birth_year__gt=min_birth_year,
    ).exclude(id__in=sid_list)[:limit]       #使用exclude排除id在那些被滑过用户的列表中,limit是取出几个

    return rcmd_users


def like_someone(user,sid):
    '''添加滑动记录'''
    Swiped.swipe(user.id,sid,s_type='like')

    #判断对方是否喜欢过
    if Swiped.is_liked(sid,user.id):
        Friend.make_friends(sid,user.id)
        return True
    else:
        return False


def superlike_someone(user,sid):
    '''添加滑动记录'''
    Swiped.swipe(user.id,sid,s_type='superlike')

    # 判断对方是否喜欢过
    if Swiped.is_liked(sid,user.id):
        Friend.make_friends(sid,user.id)
        return True
    else:
        return False



def rewind(user):
    '''反悔操作'''
    key=keys.REWIND_KEY%user.id
    rewind_num=cache.get(key,0)
    print(rewind_num)
    rewind_limit=config.REWIND_LIMIT    #最大反悔次数
    '''如果反悔次数大于或等于最大次数抛出异常'''
    if rewind_num >=rewind_limit:
        raise errors.RewindLimitErr
    '''判断最近一次滑动是否是好友'''
    swiped_latest=Swiped.objects.filter(uid=user.id).latest('s_time')       #获取当前用户最近的一次滑动记录
    if swiped_latest.s_type in ['like','superlike']:   #判断最新一次滑动是否是喜欢或者超级喜欢,如果是删除好友
        Friend.remove_friend(user.id,swiped_latest.sid)  #如果不是好友,不执行任何操作

    '''删除最近一条记录'''
    swiped_latest.delete()


    '''获取当天还剩多少时间设置过期时间'''
    now_time=datetime.datetime.now().time()   #获取当前时间的时分秒
    time=86400-3600*now_time.hour-60*now_time.minute-now_time.second  #获取今天还剩多少秒
    # '''重设缓存'''
    rewind_num+=1

    cache.set(key,rewind_num,time)


