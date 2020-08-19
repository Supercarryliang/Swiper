
# Create your views here.
from django.core.cache import cache
from django.http import HttpResponse

from libs.https import render_json
from social import logic
from social.logic import get_recommond_list, like_someone, superlike_someone
from social.models import Swiped, Friend
from user.models import User


def get_recommond(request):
    '''获取推荐用户'''
    users=get_recommond_list(request.user,10)
    data=[user.to_dict() for user in users ] #将推荐用户的信息转成json格式
    return render_json(data)


def dislike(request):
    '''滑动不喜欢的人'''
    sid=int(request.POST.get('sid'))   #获取请求中你滑动的用户id
    Swiped.swipe(request.user.id,sid,'dislike')
    print(cache.get('rewind_key3'))
    return render_json()


def like(request):
    '''滑动喜欢的人'''
    sid=int(request.POST.get('sid'))   #获取请求中你滑动的用户id
    matched=like_someone(request.user,sid)  #返回匹配的结果，True or False
    return render_json({'is_matched':matched})

def superlike(request):
    '''滑动超级喜欢的人'''
    sid=int(request.POST.get('sid'))   #获取请求中你滑动的用户id
    matched=superlike_someone(request.user,sid)
    return render_json({'is_matched':matched})

def get_friends(request):
    friends_info=request.user.friends
    return render_json(friends_info)


def rewind(request):
    logic.rewind(request.user)
    return render_json()


def get_liked_me(request):
    '''获取谁喜欢过我的用户信息'''
    liked_me_uid_list=Swiped.who_liked_me(request.user.id)
    liked_users=User.objects.filter(id__in=liked_me_uid_list)
    result=[user.to_dict() for user in liked_users]
    return render_json(result)