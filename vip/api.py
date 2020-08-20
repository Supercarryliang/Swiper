from django.shortcuts import render

# Create your views here.
from libs.https import render_json
from vip.models import Vip, Permission


def show_vip_perm(request):
    vip_perm_info=[]
    vip_list=Vip.objects.all()  #获取全部的vip对象
    for vip in vip_list:
        vip_info=vip.to_dict('id') #序列化vip对象
        vip_info['perms']=[]         #为vip_info添加一个key叫'perms'
        for perm in vip.perms():
            perm_info=perm.to_dict('id')
            vip_info['perms'].append(perm_info)


        vip_perm_info.append(vip_info)
    return render_json(vip_perm_info)
