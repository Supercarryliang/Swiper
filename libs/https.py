import json

from django.conf import settings
from django.http import HttpResponse

from common.errors import OK


def render_json(data=None,code=OK):
    '''将结果渲染成一个Json数据的HttpResponse'''
    result={
        'data':data,
        'code':code
    }
    if settings.DEBUG:
        json_result=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=4)#indent是缩进
    else:
        json_result=json.dumps(result,ensure_ascii=False,separators=(':',','))

    return HttpResponse(json_result)