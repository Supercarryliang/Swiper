from django.db import models

# Create your models here.


class Vip(models.Model):
    '''Vip表'''
    name=models.CharField(max_length=10,unique=True,verbose_name='会员名字')
    level=models.IntegerField(verbose_name='会员等级')
    price=models.FloatField(verbose_name='价格')

    class Meta:
        db_table='vip'


    def perms(self):
        '''获取vip所对应的权限'''
        #获取当前vip等级对应所有的权限的id
        perm_id_list=VipPermRelation.objects.filter(vip_id=self.id).values_list('perm_id',flat=True)
        return Permission.objects.filter(id__in=perm_id_list)
    def has_perm(self,perm_name):
        '''判断是否有该权限'''
        perms=self.perms()      #获取当前所拥有的权限
        for perm in perms:
            if perm.name==perm_name:
                return True
        return False

class Permission(models.Model):
    '''权限表'''
    name=models.CharField(max_length=10,verbose_name='权限名字')
    description=models.TextField(verbose_name='权限详细简介')

    class Meta:
        db_table='permission'

class VipPermRelation(models.Model):
    '''会员权限关系表'''
    vip_id=models.IntegerField(verbose_name='会员id')
    perm_id=models.IntegerField(verbose_name='权限id')