"""Swiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from user import  api as user_api
from social import api as social_api
from vip import api as vip_api

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    #用户模块的url
    url(r'api/user/get_vcode',user_api.get_vcode),
    url(r'api/user/check_vcode',user_api.check_vcode),
    url(r'api/user/get_profile',user_api.get_profile),
    url(r'api/user/set_profile',user_api.set_profile),
    url(r'api/user/upload_avatar',user_api.upload_avatar),

    #social模块的url
    url(r'api/social/get_recommond',social_api.get_recommond),
    url(r'api/social/dislike',social_api.dislike),
    url(r'api/social/like',social_api.like),
    url(r'api/social/superlike',social_api.superlike),
    url(r'api/social/get_friends',social_api.get_friends),
    url(r'api/social/rewind',social_api.rewind),
    url(r'api/social/get_liked_me',social_api.get_liked_me),



    url(r'api/vip/show_vip_perm',vip_api.show_vip_perm),



]
