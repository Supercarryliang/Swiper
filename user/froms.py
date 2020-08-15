from django import forms

from user.models import Profile


class Profile_Form(forms.ModelForm):  #forms.ModelForm可以使用原信息来关联相关的模型
    #此时需要写profile的所有字段  所以用class Meta来实现
    class Meta:
        model=Profile  #与from关联的类
        fields=['location','dating_sex','min_distance','max_distance',
                'min_dating_age','max_dating_age','vibration','only_matche','auto_play']#关联的字段

        #进行符合现实的逻辑判断

    def clean_max_distance(self):
        cleaned_data = super().clean() # 通过调用父类的clean方法返回清洗过的数据
        print(cleaned_data)
        if cleaned_data['min_distance'] > cleaned_data['max_distance']:
            raise forms.ValidationError('最小距离min_distance不能大于最大距离max_distance')  # 通过抛出一个异常来提醒
        else:
            return cleaned_data['max_distance']

    def clean_max_dating_age(self):
        cleaned_data = super().clean()  # 通过调用父类的clean方法返回清洗过的数据
        if cleaned_data['min_dating_age'] > cleaned_data['max_dating_age']:
            raise forms.ValidationError('最小交友年龄min_dating_age不能大于最大交友年龄max_dating_age')

        else:
            return cleaned_data['max_dating_age']
