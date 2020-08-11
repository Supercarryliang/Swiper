from common.errors import OK


def render_json(data=None,code=OK):
    '''将结果渲染成一个Json数据的HttpResponse'''