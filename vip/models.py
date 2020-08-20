from django.db import models

# Create your models here.

class Vip(models.Model):
    '''Vip表'''
    name=models.CharField(max_length=10,unique=True,verbose_name='会员名字')
    level=models.IntegerField(verbose_name='会员等级')
    price=models.FloatField(verbose_name='价格')

    class Meta:
        db_table='vip'


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