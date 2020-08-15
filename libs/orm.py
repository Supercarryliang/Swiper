class ModelMixin():
    def to_dict(self,*exclude):
        dict_list={}
        for field in self._meta.fields:  #遍历当前对象的所有属性值
            name=field.attname           #获取所有属性的名字
            if name not in exclude:      #如果属性不在忽略的名单内就放入到字典中显示
                dict_list[name]=getattr(self,name)
        return dict_list
